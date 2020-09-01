import psycopg2
import pytest
import sqlalchemy
import sqlalchemy_utils

# the pg_is_responsive function relies on a setup dictionary like the one that we defined in the docker_setup fixture
# (the input argument is aptly named the same way) and
# returns a boolean after having checked if it is possible to establish a connection with the server.
from rentomatic.repository.postgres_objects import Base, Room


def pg_is_responsive(ip, docker_setup):
    try:
        conn = psycopg2.connect(
            "host={} user={} password={} dbname={}".format(
                ip, docker_setup["postgres"]["user"], docker_setup["postgres"]["password"], "postgres"
            )
        )
        conn.close()
        return True
    except psycopg2.OperationalError as exp:
        return False


# The second fixture receives docker_services, which spins up docker-compose automatically using the docker_compose_file
# fixture I defined previously.
# The pg_is_responsive function is used to wait for the container to reach a running state,
# then a connection is established and the database is created.
# To simplify this last operation I imported and used the package sqlalchemy_utils.
# The fixture yields the SQLAlchemy engine object, so it can be correctly closed once the session is finished.


@pytest.fixture(scope="session")
def pg_engine(docker_ip, docker_services, docker_setup):
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: pg_is_responsive(docker_ip, docker_setup)
    )
    conn_str = "postgresql+psycopg2://{}:{}@{}/{}".format(
        docker_setup["postgres"]["user"],
        docker_setup["postgres"]["password"],
        docker_setup["postgres"]["host"],
        docker_setup["postgres"]["dbname"],
    )
    engine = sqlalchemy.create_engine(conn_str, pool_pre_ping=True, pool_recycle=300,)
    sqlalchemy_utils.create_database(engine.url)
    conn = engine.connect()
    yield engine
    conn.close()


@pytest.fixture(scope="session")
def pg_session_empty(pg_engine):
    Base.metadata.create_all(pg_engine)
    Base.metadata.bind = pg_engine
    DBSession = sqlalchemy.orm.sessionmaker(bind=pg_engine)
    session = DBSession()
    yield session
    session.close()


@pytest.fixture(scope="function")
def pg_data():
    return [
        {
            "code": "f853578c-fc0f-4e65-81b8-566c5dffa35a",
            "size": 215,
            "price": 39,
            "longitude": -0.09998975,
            "latitude": 51.75436293,
        },
        {
            "code": "fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a",
            "size": 405,
            "price": 66,
            "longitude": 0.18228006,
            "latitude": 51.74640997,
        },
        {
            "code": "913694c6-435a-4366-ba0d-da5334a611b2",
            "size": 56,
            "price": 60,
            "longitude": 0.27891577,
            "latitude": 51.45994069,
        },
        {
            "code": "eed76e77-55c1-41ce-985d-ca49bf6c0585",
            "size": 93,
            "price": 48,
            "longitude": 0.33894476,
            "latitude": 51.39916678,
        },
    ]


# Note that this last fixture has a function scope, thus it is run for every test.
# Therefore, we delete all rooms after the yield returns, leaving the database in the same state it had before the test


@pytest.fixture(scope="function")
def pg_session(pg_session_empty, pg_data):
    for r in pg_data:
        new_room = Room(
            code=r["code"], size=r["size"], price=r["price"], longitude=r["longitude"], latitude=r["latitude"]
        )
        pg_session_empty.add(new_room)
        pg_session_empty.commit()
    yield pg_session_empty
    pg_session_empty.query(Room).delete()
