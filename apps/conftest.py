import mongomock
from mongoengine import connect, disconnect, get_connection


def pytest_configure() -> None:
    disconnect()  # Disconnect from the default database
    connect(
        db="mongoenginetest",
        host="mongodb://localhost",
        mongo_client_class=mongomock.MongoClient,
        UuidRepresentation="standard",
    )


def pytest_runtest_teardown() -> None:
    get_connection().drop_database("mongoenginetest")


def pytest_sessionfinish() -> None:
    disconnect()
