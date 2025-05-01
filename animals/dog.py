# animals/dog.py

from animals.rescue_animal import RescueAnimal

# Dog class for dog data
class Dog(RescueAnimal):
    def __init__(self, name, breed, gender, age, weight, acquisition_date, acquisition_country,
                 training_status, reserved, in_service_country):
        super().__init__(name, gender, age, weight, acquisition_date, acquisition_country,
                         training_status, reserved, in_service_country)

        self._breed = breed
        self._animal_type = 'Dog'

    # Getters/Setters for Dog class
    @property
    def breed(self):
        return self._breed

    @breed.setter
    def breed(self, dog_breed):
        self._breed = dog_breed


