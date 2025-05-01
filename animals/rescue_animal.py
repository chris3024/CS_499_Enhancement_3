# animal/animal_rescue.py

# Parent animal class
class RescueAnimal:
    def __init__(self, name, gender, age, weight, acquisition_date,
                 acquisition_country, training_status, reserved, in_service_country):

        self._name = name
        self._gender = gender
        self._age = age
        self._weight = weight
        self._acquisition_date = acquisition_date
        self._acquisition_country = acquisition_country
        self._training_status = training_status
        self._reserved = reserved
        self._in_service_country = in_service_country
        self._animal_type = None

    # Setters and Getters for the class
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value):
        self._gender = value

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        self._age = value

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._weight = value

    @property
    def acquisition_date(self):
        return self._acquisition_date

    @acquisition_date.setter
    def acquisition_date(self, value):
        self._acquisition_date = value

    @property
    def acquisition_country(self):
        return self._acquisition_country

    @acquisition_country.setter
    def acquisition_country(self, value):
        self._acquisition_country = value

    @property
    def training_status(self):
        return self._training_status

    @training_status.setter
    def training_status(self, value):
        self._training_status = value

    @property
    def reserved(self):
        return self._reserved

    @reserved.setter
    def reserved(self, value):
        self._reserved = value

    @property
    def in_service_country(self):
        return self._in_service_country

    @in_service_country.setter
    def in_service_country(self, value):
        self._in_service_country = value

    @property
    def animal_type(self):
        return self._animal_type