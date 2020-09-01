import pytest

from rentomatic.repository import postgresrepo
from rentomatic.repository.postgres_objects import Room

pytestmark = pytest.mark.integration


def test_dummy(pg_session):
    assert len(pg_session.query(Room).all()) == 4


def test_repository_list_without_parameters(docker_setup, pg_data, pg_session):
    repo = postgresrepo.PostgresRepo(docker_setup["postgres"])
    repo_rooms = repo.list()

    assert set([r.code for r in repo_rooms]) == set([r["code"] for r in pg_data])


def test_repository_list_with_code_equal_filter(docker_setup, pg_data, pg_session):
    repo = postgresrepo.PostgresRepo(docker_setup["postgres"])
    repo_rooms = repo.list(filters={"code__eq": "fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a"})

    assert len(repo_rooms) == 1
    assert repo_rooms[0].code == "fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a"


def test_repository_list_with_price_equal_filter(docker_setup, pg_data, pg_session):
    repo = postgresrepo.PostgresRepo(docker_setup["postgres"])
    repo_rooms = repo.list(filters={"price__eq": 60})

    assert len(repo_rooms) == 1
    assert repo_rooms[0].code == "913694c6-435a-4366-ba0d-da5334a611b2"


def test_repository_list_with_price_less_than_filter(docker_setup, pg_data, pg_session):
    repo = postgresrepo.PostgresRepo(docker_setup["postgres"])
    repo_rooms = repo.list(filters={"price__lt": 60})

    assert len(repo_rooms) == 2
    assert set([r.code for r in repo_rooms]) == {
        "f853578c-fc0f-4e65-81b8-566c5dffa35a",
        "eed76e77-55c1-41ce-985d-ca49bf6c0585",
    }


def test_repository_list_with_price_greater_than_filter(docker_setup, pg_data, pg_session):
    repo = postgresrepo.PostgresRepo(docker_setup["postgres"])
    repo_rooms = repo.list(filters={"price__gt": 48})

    assert len(repo_rooms) == 2
    assert set([r.code for r in repo_rooms]) == {
        "913694c6-435a-4366-ba0d-da5334a611b2",
        "fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a",
    }


def test_repository_list_with_price_between_filter(docker_setup, pg_data, pg_session):
    repo = postgresrepo.PostgresRepo(docker_setup["postgres"])
    repo_rooms = repo.list(filters={"price__lt": 66, "price__gt": 48})

    assert len(repo_rooms) == 1
    assert repo_rooms[0].code == "913694c6-435a-4366-ba0d-da5334a611b2"
