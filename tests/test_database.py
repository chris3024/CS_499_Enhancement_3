"""
tests.test_database
Tests for the database
"""
import bcrypt
import pytest
from bson.objectid import ObjectId
from datetime import date

def _sample_dog_dict(**overrides):
    base = {
        "name": "Buddy",
        "animal_type": "Dog",
        "breed": "Labrador",
        "gender": "Male",
        "age": 2,
        "weight": 25.0,
        "acquisition_country": "USA",
        "training_status": "Not Trained",
        "reserved": False,
        "in_service_country": "USA",
        "acquisition_date": date.today().isoformat(),
    }
    base.update(overrides)
    return base

# ---------------------------------------------------------------------------

def test_create_user_and_authenticate(db):
    db.create_user("jane", "pwd123", role="user", first_login=False)
    user, first = db.authenticate_user("jane", "pwd123")
    assert user and user["username"] == "jane"
    assert first is False
    # password must be stored hashed
    assert bcrypt.checkpw("pwd123".encode(), user["password"])

def test_duplicate_user_raises(db):
    db.create_user("john", "p", role="user", first_login=False)
    with pytest.raises(ValueError):
        db.create_user("john", "p", role="user", first_login=False)

def test_full_animal_crud_cycle(db):
    # CREATE
    dog = _sample_dog_dict()
    assert db.create_animal(dog) is True

    # READ
    animals = db.read_all_animals({"name": "Buddy"})
    assert len(animals) == 1
    created_id = animals[0]["_id"]
    assert isinstance(created_id, ObjectId)

    # UPDATE
    assert db.update_animal(created_id, {"reserved": True}) is True
    updated = db.read_all_animals({"_id": created_id})[0]
    assert updated["reserved"] is True

    # DELETE
    assert db.delete_animal(created_id) is True
    assert db.read_all_animals({"_id": created_id}) == []
