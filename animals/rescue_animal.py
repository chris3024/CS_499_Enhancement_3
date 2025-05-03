"""
animals.rescue_animal
Base class for all rescue animals.
"""

from __future__ import annotations

from datetime import date, datetime
import math
from typing import Any, Dict

# Parent animal class
class RescueAnimal:
    def __init__(self, *, name: str, gender: str, age: int, weight: float,
                 acquisition_country: str, training_status: str, reserved: bool,
                 in_service_country: str) -> None:

        self.name = name
        self.gender = gender
        self.age = age
        self.weight = weight
        self._acquisition_date: str = date.today().isoformat()
        self.acquisition_country = acquisition_country
        self.training_status = training_status
        self.reserved = reserved
        self.in_service_country = in_service_country


    # Validation helpers
    @staticmethod
    def _non_empty(value: str, field: str) -> str:
        if not value or not value.strip():
            raise ValueError(f"{field} cannot be empty")
        return value.strip().title()

    @staticmethod
    def _positive_int(value: int, field: str) -> int:
        if not isinstance(value, int) or value < 0:
            raise ValueError(f"{field} must be non-negative integer")
        return value

    @staticmethod
    def _positive_float(value: float, field: str) -> float:
        try:
            num = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{field} must be numeric") from exc
        if num <= 0 or math.isnan(num) or math.isinf(num):
            raise ValueError(f"{field} must be positive")
        return num

    # Setters and Getters for the class
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = self._non_empty(value, "name")

    @property
    def gender(self) -> str:
        return self._gender

    @gender.setter
    def gender(self, value: str) -> None:
        self._gender = self._non_empty(value, "gender")

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        self._age = self._positive_int(value, "age")

    @property
    def weight(self) -> float:
        return self._weight

    @weight.setter
    def weight(self, value: float) -> None:
        self._weight = self._positive_float(value, "weight")

    @property
    def acquisition_date(self) -> str:
        """ISO 8601 date when the animal record was created."""
        return self._acquisition_date

    @property
    def acquisition_country(self) -> str:
        return self._acquisition_country

    @acquisition_country.setter
    def acquisition_country(self, value: str) -> None:
        self._acquisition_country = self._non_empty(value, "acquisition_country")

    @property
    def training_status(self) -> str:
        return self._training_status

    @training_status.setter
    def training_status(self, value: str) -> None:
        self._training_status = self._non_empty(value, "training_status")

    @property
    def reserved(self) -> bool:
        return self._reserved

    @reserved.setter
    def reserved(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise ValueError("reserved must be a boolean")
        self._reserved = value

    @property
    def in_service_country(self) -> str:
        return self._in_service_country

    @in_service_country.setter
    def in_service_country(self, value: str) -> None:
        self._in_service_country = self._non_empty(value, "in_service_country")

    def to_dict(self) -> Dict[str, Any]:
        """Return a dict representation of this animal."""
        return {
            "name": self.name,
            "gender": self.gender,
            "age": self.age,
            "weight": self.weight,
            "acquisition_date": self.acquisition_date,
            "acquisition_country": self.acquisition_country,
            "training_status": self.training_status,
            "reserved": self.reserved,
            "in_service_country": self.in_service_country,
            "animal_type": getattr(self.__class__, "animal_type", None),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> RescueAnimal:
        """Factory for quickly rebuilding objects from database"""
        obj = cls(
            name=data["name"],
            gender=data["gender"],
            age=int(data["age"]),
            weight=float(data["weight"]),
            acquisition_country=data["acquisition_country"],
            training_status=data["training_status"],
            reserved=bool(data["reserved"]),
            in_service_country=data["in_service_country"],
        )
        # restoring the original acquisition date
        obj._acquisition_date = data["acquisition_date"]
        return obj

    # Dunder Helper
    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} name={self.name!r} "
            f"age={self.age} reserved={self.reserved}> "
        )