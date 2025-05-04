"""
animals.dog
Defines the Dog subclass of RescueAnimal
"""

from __future__ import annotations
from animals.rescue_animal import RescueAnimal

# Dog class for dog data
class Dog(RescueAnimal):

    animal_type = "Dog"

    def __init__(self, *, name: str, breed: str, gender: str, age: int, weight: float,
                 acquisition_country: str, training_status: str, reserved: bool, in_service_country: str)-> None:
        super().__init__(
            name=name,
            gender=gender,
            age=age,
            weight=weight,
            acquisition_country=acquisition_country,
            training_status=training_status,
            reserved=reserved,
            in_service_country=in_service_country)

        self.breed = breed


    # Getters/Setters for Dog class
    @property
    def breed(self) -> str:
        return self._breed

    @breed.setter
    def breed(self, value: str) -> None:
        if not value:
            raise ValueError("breed cannot be empty")
        self._breed = value.title().strip()

    # Converting object to dict for database
    def to_dict(self) -> dict[str, object]:
        base = super().to_dict()
        base.update({"breed": self.breed, "animal_type": self.animal_type})
        return base
