"""
animals.dog
Holds the Dog subclass information
"""

from animals.rescue_animal import RescueAnimal

class Dog(RescueAnimal):
    animal_type = "Dog"

    def __init__(self, *, name: str, breed: str, gender: str, age: int, weight: float,
                 acquisition_country: str, training_status: str, reserved: bool, in_service_country: str):
        super().__init__(
            name=name,
            gender=gender,
            age=age,
            weight=weight,
            acquisition_country=acquisition_country,
            training_status=training_status,
            reserved=reserved,
            in_service_country=in_service_country
        )
        self.breed = breed.strip().title()

    def to_dict(self):
        data = super().to_dict()
        data["breed"] = self.breed
        return data
