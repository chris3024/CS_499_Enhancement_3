from datetime import date
from typing import Any, Dict
import math

class RescueAnimal:
    __slots__ = (
        "_name", "_gender", "_age", "_weight", "_acquisition_date",
        "_acquisition_country", "_training_status", "_reserved", "_in_service_country"
    )

    def __init__(self, *, name: str, gender: str, age: int, weight: float,
                 acquisition_country: str, training_status: str, reserved: bool,
                 in_service_country: str) -> None:
        self.name = name
        self.gender = gender
        self.age = age
        self.weight = weight
        self._acquisition_date = date.today().isoformat()
        self.acquisition_country = acquisition_country
        self.training_status = training_status
        self.reserved = reserved
        self.in_service_country = in_service_country

    @staticmethod
    def _validate_str(value: str, field: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} must be a non-empty string")
        return value.strip().title()

    @staticmethod
    def _validate_int(value: int, field: str) -> int:
        if not isinstance(value, int) or value < 0:
            raise ValueError(f"{field} must be a non-negative integer")
        return value

    @staticmethod
    def _validate_float(value: float, field: str) -> float:
        try:
            val = float(value)
        except (TypeError, ValueError):
            raise ValueError(f"{field} must be a valid float")
        if val <= 0 or math.isnan(val) or math.isinf(val):
            raise ValueError(f"{field} must be a positive number")
        return val

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = self._validate_str(value, "name")

    @property
    def gender(self) -> str:
        return self._gender

    @gender.setter
    def gender(self, value: str) -> None:
        self._gender = self._validate_str(value, "gender")

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        self._age = self._validate_int(value, "age")

    @property
    def weight(self) -> float:
        return self._weight

    @weight.setter
    def weight(self, value: float) -> None:
        self._weight = self._validate_float(value, "weight")

    @property
    def acquisition_date(self) -> str:
        return self._acquisition_date

    @property
    def acquisition_country(self) -> str:
        return self._acquisition_country

    @acquisition_country.setter
    def acquisition_country(self, value: str) -> None:
        self._acquisition_country = self._validate_str(value, "acquisition_country")

    @property
    def training_status(self) -> str:
        return self._training_status

    @training_status.setter
    def training_status(self, value: str) -> None:
        self._training_status = self._validate_str(value, "training_status")

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
        self._in_service_country = self._validate_str(value, "in_service_country")

    def to_dict(self) -> Dict[str, Any]:
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
    def from_dict(cls, data: Dict[str, Any]) -> "RescueAnimal":
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
        obj._acquisition_date = data.get("acquisition_date", date.today().isoformat())
        return obj

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r} age={self.age} reserved={self.reserved}>"
