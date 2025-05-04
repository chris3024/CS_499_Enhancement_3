"""
test.test_animals
Testing the animal classes
"""
import pytest
from animals.dog import Dog
from animals.monkey import Monkey


def test_dog_to_dict_contains_expected_keys():
    dog = Dog(
        name="Rex",
        breed="Labrador",
        gender="Male",
        age=3,
        weight=30.5,
        acquisition_country="USA",
        training_status="In Training",
        reserved=False,
        in_service_country="USA",
    )
    d = dog.to_dict()
    assert d["animal_type"] == "Dog"
    assert d["breed"] == "Labrador"
    assert d["name"] == "Rex"

def test_monkey_to_dict_contains_expected_keys():
    m = Monkey(
        name="Zuri",
        species="Capuchin",
        gender="Female",
        age=4,
        weight=8.2,
        acquisition_country="Brazil",
        training_status="Not Trained",
        reserved=True,
        in_service_country="Canada",
    )
    d = m.to_dict()
    assert d["animal_type"] == "Monkey"
    assert d["species"] == "Capuchin"


def test_negative_age_raises_value_error():
    with pytest.raises(ValueError):
        Dog(
            name="Rex",
            breed="Lab",
            gender="Male",
            age=-1,                   # invalid
            weight=10,
            acquisition_country="USA",
            training_status="In Training",
            reserved=False,
            in_service_country="USA",
        )
