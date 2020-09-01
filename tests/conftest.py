import os
import tempfile

import pytest
import yaml

from rentomatic.app import create_app
from rentomatic.flask_settings import TestConfig


@pytest.yield_fixture(scope="function")
def app():
    return create_app(TestConfig)


# The first function is a hook into the pytest CLI parser that adds the --integration option.
# When this option is specified on the command line the pytest setup will contain the key integration with value True.


def pytest_addoption(parser):
    parser.addoption("--integration", action="store_true", help="run integration tests")


# The second function is a hook into the pytest setup of every single test.
# The item variable contains the test itself (actually a _pytest.python.Function object),
# which in turn contains two useful pieces of information.
#
# The first is the item.keywords attribute, that contains the test marks,
# alongside many other interesting things like the name of the test, the file, the module,
# and also information about the patches that happen inside the test.
#
# The second is the item.config attribute that contains the parsed pytest command line.


def pytest_runtest_setup(item):
    if "integration" in item.keywords and not item.config.getvalue("integration"):
        pytest.skip("need --integration option to run")


@pytest.fixture(scope="session")
def docker_setup(docker_ip):
    return {
        "postgres": {"dbname": "rentomaticdb", "user": "postgres", "password": "rentomaticdb", "host": docker_ip},
        "mongo": {"dbname": "rentomaticdb", "user": "root", "password": "rentomaticdb", "host": docker_ip},
    }


@pytest.fixture(scope="session")
def docker_tmpfile():
    f = tempfile.mkstemp()
    yield f
    os.remove(f[1])


@pytest.fixture(scope="session")
def docker_compose_file(docker_tmpfile, docker_setup):
    content = {
        "version": "3.1",
        "services": {
            "postgresql": {
                "restart": "always",
                "image": "postgres",
                "ports": ["5432:5432"],
                "environment": ["POSTGRES_PASSWORD={}".format(docker_setup["postgres"]["password"])],
            },
            "mongo": {
                "restart": "always",
                "image": "mongo",
                "ports": ["27017:27017"],
                "environment": [
                    "MONGO_INITDB_ROOT_USERNAME={}".format(docker_setup["mongo"]["user"]),
                    "MONGO_INITDB_ROOT_PASSWORD={}".format(docker_setup["mongo"]["password"]),
                ],
            },
        },
    }
    f = os.fdopen(docker_tmpfile[0], "w")
    f.write(yaml.dump(content))
    f.close()
    return docker_tmpfile[1]
