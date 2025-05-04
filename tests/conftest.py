# tests/conftest.py
import mongomock
import pytest

from data.database_manager import AnimalDatabase

@pytest.fixture()
def db(monkeypatch):
    """
    Return an AnimalDatabase wired to an in‑memory (mongomock) client
    instead of a real MongoDB server.
    """
    monkeypatch.setattr(
        "data.database_manager.MongoClient",  # where MongoClient is imported
        mongomock.MongoClient,
        raising=True,
    )
    # URI is ignored because we've patched the class above
    return AnimalDatabase(mongo_uri="mongodb://dummy")
