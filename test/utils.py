import pytest
from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker
from database import Base
from fastapi.testclient import TestClient
from router.auth import bcrypt_context

from main import app
from models import Todos, Users

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread" : False}, poolclass=StaticPool)

TestSessionLocal = sessionmaker(autoflush=False, autocommit=False, bind = engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db

    finally:
        db.close()

def override_get_current_user():
    return {'username': 'rugged_code', 'id': 1, 'role': 'admin'}

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to code!",
        description="Need to learn everyday!",
        priority=5,
        completed=False,
        owner_id=1,
    )
    db = TestSessionLocal()
    db.add(todo)
    db.commit()
    yield todo

    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()

@pytest.fixture
def test_user():
    user = Users(
        username='ruggedcode',
        email='ruggedcode@email.com',
        first_name='Shrey',
        last_name='Raj',
        hashed_password=bcrypt_context.hash("testpass"),
        role='admin',
        phone_number='9090767689'
    )

    db = TestSessionLocal()
    db.add(user)
    db.commit()

    yield user
    with engine.connect() as conn:
        conn.execute(text("DELETE from users;"))
        conn.commit()

