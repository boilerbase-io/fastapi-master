# load env
TEST_ENV_PATH = "./tests/.test_env"

from dotenv import load_dotenv

load_dotenv(TEST_ENV_PATH)

# load tables to create
from src.user.models import User


# necessary imports
import os
import uuid
import pytest
import psycopg2

from typing import Generator
from utils.db.base import ModelBase
from pytest import FixtureRequest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from sqlalchemy.engine.base import Engine
from fastapi import FastAPI, HTTPException
from psycopg2.errors import DuplicateDatabase, InvalidCatalogName

from fastapi import Header, Depends
from utils.db.session import get_db
from sqlalchemy import create_engine
from pytest_factoryboy import register
from src.main import create_app
from src.user.utils.deps import authenticated_user

from typing import Any
from src.user.crud import crud_user
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Factory imports
from tests.factory import (
    LikeFactory,
    UserFactory,
    UsageFactory,
    UserLogFactory,
    FeedbackFactory,
    ModifierFactory,
    ServicesFactory,
    GenerationFactory,
    PreferencesFactory,
)


# load env vars
DEFAULT_DB_NAME = "postgres"
DB_PORT = os.getenv("POSTGRES_PORT", 5777)
DB_NAME = os.getenv("POSTGRES_DB", "pytest_db")
DB_HOST = os.getenv("POSTGRES_SERVER", "localhost")
DB_USERNAME = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "mysecretpassword")
DEFAULT_DB_URL = (
    f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

SQLALCHEMY_DATABASE_URL = os.getenv("TEST_DATABASE_URL", DEFAULT_DB_URL)


@pytest.fixture(scope="session", autouse=True)
def create_db():
    con = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        dbname=DEFAULT_DB_NAME,
    )
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = con.cursor()

    # Create and delete table statement
    create_db_q = f"CREATE DATABASE {DB_NAME};"
    drop_db_q = f"DROP DATABASE {DB_NAME} WITH (FORCE);"

    # Create a table in PostgreSQL database
    try:
        cursor.execute(create_db_q)
    except DuplicateDatabase:
        print("DB is already there recreating it.")
    finally:
        cursor.execute(drop_db_q)
        cursor.execute(create_db_q)

    yield

    # Create a table in PostgreSQL database
    try:
        cursor.execute(drop_db_q)
    except InvalidCatalogName:
        print("DB is not there. So, can not delete it.")
    finally:
        print('"psycopg2" Connection closed.')


@pytest.fixture(scope="function")
def engine():
    return create_engine(SQLALCHEMY_DATABASE_URL)


@pytest.fixture(scope="function")
def db_session(engine: Engine) -> Generator[Session, Any, None]:
    """
    Creates a fresh sqlalchemy session for each test that operates in a
    transaction. The transaction is rolled back at the end of each test ensuring
    a clean state.
    """

    # connect to the database
    connection = engine.connect()
    # begin a non-ORM transaction
    transaction = connection.begin()
    # bind an individual Session to the connection
    session = Session(bind=connection)

    yield session  # use the session in tests.

    session.close()
    # rollback - everything that happened with the
    # Session above (including calls to commit())
    # is rolled back.
    transaction.rollback()
    # return connection to the Engine
    connection.close()
    engine.dispose()


@pytest.fixture(scope="function")
def persistent_db_session(engine: Engine) -> Generator[Session, Any, None]:
    """
    Creates a fresh sqlalchemy session for each test that operates in a
    transaction. The transaction is rolled back at the end of each test ensuring
    a clean state.
    """

    # connect to the database
    connection = engine.connect()
    # bind an individual Session to the connection
    session = Session(bind=connection)

    yield session  # use the session in tests.

    session.close()
    # return connection to the Engine
    connection.close()
    engine.dispose()


@pytest.fixture(scope="function")
def app(engine: Engine) -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    ModelBase.metadata.create_all(bind=engine)  # Create the tables.
    _app = create_app(env_path=TEST_ENV_PATH)

    yield _app

    ModelBase.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def client(app: FastAPI, db_session: Session) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    def _authenticated_user(
        session_token: str = Header(None), db: Session = Depends(_get_test_db)
    ):
        user_id = session_token
        try:
            user = crud_user.get_by_id(db, id=user_id)
            if user:
                return db, user
            else:
                raise HTTPException(401, "Not a valid user")
        except Exception:
            raise HTTPException(401, "Not a valid token")

    app.dependency_overrides[get_db] = _get_test_db
    app.dependency_overrides[authenticated_user] = _authenticated_user
    with TestClient(app) as client:
        yield client


# Fixture for Seeding the data to database
@pytest.fixture
def seed(request: FixtureRequest, persistent_db_session: Session):
    marker = request.node.get_closest_marker("seed_data")
    if not (marker and marker.args and isinstance(marker.args, tuple)):
        print("_______________________________________________________")
        print("    There is no seed data or not a valid seed data.    ")
        print("-------------------------------------------------------")
        assert False

    for dataset in marker.args:
        entity_name, overridden_attributes = dataset

        # Attributes can either be passed as a:
        #   * `dict` if there is only one entity record to be seeded
        #   * `list` if there are multiple entity recores to be seeded
        if isinstance(overridden_attributes, dict):
            factory = request.getfixturevalue(entity_name + "_factory")
            pytest.persist_object(
                persistent_db_session, factory(**overridden_attributes)
            )
        elif isinstance(overridden_attributes, list):
            for attribute_set in overridden_attributes:
                factory = request.getfixturevalue(entity_name + "_factory")
                pytest.persist_object(persistent_db_session, factory(**attribute_set))


IDENTIFIERS = {}


def persist_object(db: Session, object):
    db.add(object)
    db.commit()
    return object


def id_for(key):
    if key not in IDENTIFIERS:
        IDENTIFIERS[key] = str(uuid.uuid4())
    return IDENTIFIERS[key]


pytest.id_for = id_for
pytest.persist_object = persist_object


# register factories
register(UserFactory)
register(LikeFactory)
register(UsageFactory)
register(UserLogFactory)
register(ModifierFactory)
register(FeedbackFactory)
register(ServicesFactory)
register(GenerationFactory)
register(PreferencesFactory)


@pytest.fixture
def persisted_user(persistent_db_session, user):
    return pytest.persist_object(persistent_db_session, user)


@pytest.fixture
def persisted_admin_user(persistent_db_session, user):
    user.is_admin = True
    return pytest.persist_object(persistent_db_session, user)
