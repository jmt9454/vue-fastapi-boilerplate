import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base
from app.routers.students import get_db

# 1. Create an In-Memory SQLite Database
# "check_same_thread=False" is needed for SQLite in tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# 2. Create a Testing Session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Fixture: Setup the DB before tests, Tear it down after
@pytest.fixture(name="session")
def db_session():
    # Create tables in the memory DB
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop tables after tests (optional with memory DB, but good practice)
        Base.metadata.drop_all(bind=engine)

# 4. Fixture: The TestClient that uses the overridden DB
@pytest.fixture(name="client")
def client_fixture(session):
    # Define the override
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    # Apply the override
    app.dependency_overrides[get_db] = override_get_db
    
    # Return the TestClient
    yield TestClient(app)
    
    # Clear overrides
    app.dependency_overrides.clear()