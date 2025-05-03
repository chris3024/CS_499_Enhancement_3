"""
animals.monkey
Defines the Monkey subclass of RescueAnimal
"""

from __future__ import annotations
from animals.rescue_animal import RescueAnimal

# Monkey class for Monkey data
class Monkey(RescueAnimal):

    animal_type = 'Monkey'

    def __init__(self, *, name: str, species: str, tail_length: float, height: float, body_length: float, gender: str,
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
        self.tail_length = tail_length
        self.height = height
        self.body_length = body_length

    # Getters/Setters for Monkey class
    @property
    def species(self) -> str:
        return self._species

    @species.setter
    def species(self, value: str) -> None:
        if not value:
            raise ValueError("species cannot be empty")
        self._species = value.title().strip()

    @property
    def tail_length(self) -> float:
        return self._tail_length

    @tail_length.setter
    def tail_length(self, value: float | str) -> None:
        self._tail_length = self._validate_positive_float(value, "tail_length")

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value: float | str) -> None:
        self._height = self._validate_positive_float(value, "height")

    @property
    def body_length(self) -> float:
        return self._body_length

    @body_length.setter
    def body_length(self, value: float | str) -> None:
        self._body_length = self._validate_positive_float(value, "body_length")

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
                "tail_length": self.tail_length,
                "height": self.height,
                "body_length": self.body_length,
                "animal_type": self.animal_type,
            }
        )
        return data