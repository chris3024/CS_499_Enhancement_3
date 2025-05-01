# animals/monkey.py

from animals.rescue_animal import RescueAnimal

# Monkey class for Monkey data
class Monkey(RescueAnimal):
    def __init__(self, name, species, tail_length, height, body_length, gender, age, weight, acquisition_date,
                 acquisition_country, training_status, reserved, in_service_country):
        super().__init__(name, gender, age, weight, acquisition_date, acquisition_country, training_status,
                         reserved, in_service_country)

        self._species = species
        self._tail_length = tail_length
        self._height = height
        self._body_length = body_length
        self._animal_type = 'Monkey'

    # Getters/Setters for Monkey class
    @property
    def species(self):
        return self._species

    @species.setter
    def species(self, value):
        self._species = value

    @property
    def tail_length(self):
        return self._tail_length

    @tail_length.setter
    def tail_length(self, value):
        self._tail_length = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def body_length(self):
        return self._body_length

    @body_length.setter
    def body_length(self, value):
        self._body_length = value