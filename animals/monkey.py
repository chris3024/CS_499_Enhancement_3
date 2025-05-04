"""
animals.monkey
Defines the Monkey subclass of RescueAnimal
"""

from __future__ import annotations
from animals.rescue_animal import RescueAnimal

# Monkey class for Monkey data
class Monkey(RescueAnimal):

    animal_type = 'Monkey'

    def __init__(self, *, name: str, species: str, gender: str,
                 age: int, weight: float, acquisition_country: str, training_status: str,
                 reserved: bool, in_service_country: str)-> None:
        super().__init__(
            name=name,
            gender=gender,
            age=age,
            weight=weight,
            acquisition_country=acquisition_country,
            training_status=training_status,
            reserved=reserved,
            in_service_country=in_service_country)

        self.species = species


    # Getters/Setters for Monkey class
    @property
    def species(self) -> str:
        return self._species

    @species.setter
    def species(self, value: str) -> None:
        if not value:
            raise ValueError("species cannot be empty")
        self._species = value.title().strip()


    @staticmethod
    def _validate_positive_float(value: float | str, field: str) -> float:
        try:
            num = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f'{field} must be a number') from exc
        if num <= 0:
            raise ValueError(f'{field} must be a positive number')
        return num

    # Converting Object to dict for database
    def to_dict(self) -> dict[str, object]:
        data = super().to_dict()
        data.update(
            {
                "species": self.species,
                "animal_type": self.animal_type,
            }
        )
        return data
