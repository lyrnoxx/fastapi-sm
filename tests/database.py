from fastapi.testclient import TestClient
from app.main import app
import pytest
from app import schemas
from app.database import get_db
from app.config import settings
from app.database import base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL =f"postgresql://{settings.database_username}:{settings.database_pass}@{settings.database_host}/{settings.database_name}_testing"

engine= create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

@pytest.fixture
def session():
    base.metadata.drop_all(bind=engine)
    base.metadata.create_all(bind=engine)
    db=TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db]= override_get_db
    yield TestClient(app)

