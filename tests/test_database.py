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

def test_create_and_authenticate_user(db):
    db.create_user("jane", "pwd123", role="user", first_login=False)
    user, first_login = db.authenticate_user("jane", "pwd123")
    assert user is not None
    assert user["username"] == "jane"
    assert first_login is False
    assert bcrypt.checkpw("pwd123".encode(), user["password"])
    assert user["password"] != "pwd123"

def test_authenticate_with_wrong_password(db):
    db.create_user("jane", "pwd123", role="user", first_login=False)
    user, _ = db.authenticate_user("jane", "wrongpassword")
    assert user is None

def test_duplicate_user_creation_raises_error(db):
    db.create_user("john", "password", role="user", first_login=False)
    with pytest.raises(ValueError):
        db.create_user("john", "password", role="user", first_login=False)

def test_create_and_read_animal(db):
    dog = _sample_dog_dict()
    assert db.create_animal(dog) is True
    animals = db.read_all_animals({"name": "Buddy"})
    assert len(animals) == 1
    retrieved = animals[0]
    assert isinstance(retrieved["_id"], ObjectId)
    assert retrieved["name"] == "Buddy"
    assert retrieved["breed"] == "Labrador"

def test_update_animal_reserved_status(db):
    dog = _sample_dog_dict()
    db.create_animal(dog)
    created = db.read_all_animals({"name": "Buddy"})[0]
    animal_id = created["_id"]
    assert db.update_animal(animal_id, {"reserved": True}) is True
    updated = db.read_all_animals({"_id": animal_id})[0]
    assert updated["reserved"] is True

def test_delete_animal_entry(db):
    dog = _sample_dog_dict()
    db.create_animal(dog)
    created = db.read_all_animals({"name": "Buddy"})[0]
    animal_id = created["_id"]
    assert db.delete_animal(animal_id) is True
    assert db.read_all_animals({"_id": animal_id}) == []
