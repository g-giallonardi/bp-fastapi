import os
import subprocess
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.database import Base
from main import app
from fastapi.testclient import TestClient
from core.config import settings

# Use an in-memory SQLite database for testing
TEST_DATABASE_URL = settings.DATABASE_URL
DB_NAME=settings.DB_NAME

# Override the test database
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Reset and migrate the test database before running tests using system commands."""
    DB_FILE = f"{DB_NAME}.db"

    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    subprocess.run(["alembic", "upgrade", "head"], check=True)

    yield

    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

@pytest.fixture(scope="session")
def db():
    Base.metadata.drop_all(bind=engine)  
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    yield session
    session.close()

@pytest.fixture(scope="module")
def client():
    """Provides a test client"""
    return TestClient(app)