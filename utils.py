from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ..database import Base
from ..main import app
from fastapi.testclient import TestClient
import pytest
from ..models import ToDos, Users
from  ..routers.auth import bcrypt_context


SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread" : False},
    poolclass= StaticPool
)

TestingSessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base.metadata.create_all(bind = engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username':'koby', 'id' : 1, 'user_role':'admin'}

client = TestClient(app)

@pytest.fixture()
def test_todo():
    todo = ToDos(
        title = "learn fastapi",
        description = "need money",
        priority = 1,
        complete = False,
        owner_id = 1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()




@pytest.fixture()
def test_user():
    user = Users(
        username = 'koby',
        email = 'koby@gmai.com',
        first_name = 'koby',
        last_name = 'israeli',
        hashed_password = bcrypt_context.hash("testpass"),
        role='admin',
        phone_number="0584176451"
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
