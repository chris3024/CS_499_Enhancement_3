"""
animals.monkey
Holds the Monkey subclass information
"""

from animals.rescue_animal import RescueAnimal

class Monkey(RescueAnimal):
    animal_type = "Monkey"

    def __init__(self, *, name: str, species: str, gender: str, age: int, weight: float,
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
        self.species = species.strip().title()

    def to_dict(self):
        data = super().to_dict()
        data["species"] = self.species
        return data
