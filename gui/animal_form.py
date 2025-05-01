# gui/animal_form.py

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from datetime import datetime
from data.data_manager import save_animals


# Class to hold new window to add a new animal
class AnimalFormWindow(tk.Toplevel):
    def __init__(self, parent, animal_type):
        super().__init__(parent)

        self.animal_type = animal_type

        self.submit_button = None
        self.service_country_entry = None
        self.species_combobox = None
        self.reserved_combobox = None
        self.training_combobox = None
        self.country_entry = None
        self.date_entry = None
        self.weight_entry = None
        self.breed_entry = None
        self.age_entry = None
        self.gender_combobox = None
        self.name_entry = None
        self.animal_frame = None

        self.title("Animal Form")
        self.geometry("400x600")
        self.resizable(False, False)

        self.add_form()

    # Form to add the animal
    def add_form(self):
        self.animal_frame = tk.LabelFrame(self, text="Add Animal")
        self.animal_frame.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")

        field_width = 30

        ttk.Label(self.animal_frame, text="Name").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.name_entry = ttk.Entry(self.animal_frame, width=field_width)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="e")

        # Determine whether animal is Dog or Monkey, sets the correct information input for Breed/Species
        if self.animal_type == "Dog":
            ttk.Label(self.animal_frame, text="Breed").grid(row=1, column=0, padx=10, pady=10, sticky="e")
            self.breed_entry = ttk.Entry(self.animal_frame, width=field_width)
            self.breed_entry.grid(row=1, column=1, padx=10, pady=5, sticky="e")
        elif self.animal_type == "Monkey":
            ttk.Label(self.animal_frame, text="Species").grid(row=1, column=0, padx=10, pady=10, sticky="e")
            self.species_combobox = ttk.Combobox(self.animal_frame, values=["Capuchin", "Guenon", "Macaque",
                                                                            "Marmoset", "Squirrel Monkey", "Tamarin"],
                                                 state="readonly",width=25)
            self.species_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="e")

        ttk.Label(self.animal_frame, text="Gender").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.gender_combobox = ttk.Combobox(self.animal_frame, values=["Male", "Female"], state="readonly",
                                            width=25)
        self.gender_combobox.grid(row=2, column=1, padx=10, pady=5, sticky="e")

        ttk.Label(self.animal_frame, text="Age").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        validate_age = self.register(self.validate_integer)
        self.age_entry = ttk.Entry(self.animal_frame, width=field_width, validate="key",
                                   validatecommand=(validate_age,"%P"))
        self.age_entry.grid(row=3, column=1, padx=10, pady=5, sticky="e")

        ttk.Label(self.animal_frame, text="Weight").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        validate_weight = self.register(self.validate_integer)
        self.weight_entry = ttk.Entry(self.animal_frame, width=field_width, validate="key",
                                      validatecommand=(validate_weight, "%P"))
        self.weight_entry.grid(row=4, column=1, padx=10, pady=5, sticky="e")

        ttk.Label(self.animal_frame, text="Acquisition Date").grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.date_entry = ttk.Entry(self.animal_frame, width=field_width)
        self.date_entry.grid(row=5, column=1, padx=10, pady=5, sticky="e")

        # Inserting current date when adding animal
        current_date = datetime.today().strftime('%Y-%m-%d')
        self.date_entry.insert(0, current_date)

        ttk.Label(self.animal_frame, text="Acquisition Country").grid(row=6, column=0, padx=10, pady=10, sticky="e")
        self.country_entry = ttk.Entry(self.animal_frame, width=field_width)
        self.country_entry.grid(row=6, column=1, padx=10, pady=5, sticky="e")
        
        ttk.Label(self.animal_frame, text="Training Status").grid(row=7, column=0, padx=10, pady=10, sticky="e")
        self.training_combobox = ttk.Combobox(self.animal_frame, values=["Not Trained", "In Training", "Fully Trained"],
                                              state="readonly", width=25)
        self.training_combobox.grid(row=7, column=1, padx=10, pady=5, sticky="e")

        ttk.Label(self.animal_frame, text="Reserved").grid(row=8, column=0, padx=10, pady=10, sticky="e")
        self.reserved_combobox = ttk.Combobox(self.animal_frame, values=["Yes", "No"], state="readonly",
                                              width=25)
        self.reserved_combobox.grid(row=8, column=1, padx=10, pady=5, sticky="e")

        ttk.Label(self.animal_frame, text="In Service Country").grid(row=9, column=0, padx=10, pady=10, sticky="e")
        self.service_country_entry = ttk.Entry(self.animal_frame, width=field_width)
        self.service_country_entry.grid(row=9, column=1, padx=10, pady=5, sticky="e")

        self.submit_button = ttk.Button(self.animal_frame, text="Submit", command=self.submit_form)
        self.submit_button.grid(row=10, column=0, padx=10, pady=5, sticky="e")
        
        
    # input validation for integers
    def validate_integer(self, value):
        if value == "" or value.isdigit():
            return True
        else:
            tk.messagebox.showerror("Error", "Please enter a valid integer.", parent=self)
            return False

    def submit_form(self):
        # Collecting the data from the form
        name = self.name_entry.get()
        age = self.age_entry.get()
        weight = self.weight_entry.get()
        gender = self.gender_combobox.get()
        date = self.date_entry.get()
        country = self.country_entry.get()
        reserved = self.reserved_combobox.get()
        training_status = self.training_combobox.get()
        service = self.service_country_entry.get()

        animal_data = {
            "name": name,
            "animal_type": self.animal_type,
            "gender": gender,
            "age": age,
            "weight": weight,
            "acquisition_date": date,
            "acquisition_country": country,
            "training_status": training_status,
            "reserved": reserved,
            "in_service_country": service

        }

        # Determining the correct information to add and location to save dependent on the animal type
        if self.animal_type == "Monkey":
            species = self.species_combobox.get()
            animal_data["species"] = species
            file_name = "data/animal_data_monkey.json"
        else:
            breed = self.breed_entry.get()
            animal_data["breed"] = breed
            file_name = "data/animal_data_dog.json"

        # Checking that fields have data entered
        if not name or not age or not weight or not gender or not date or not country or not service:
            tk.messagebox.showerror("Error", "Please fill all fields.", parent=self)
            return

        # Saving the animal to the JSON
        save_animals(file_name, animal_data)

        # Displaying message if success
        tk.messagebox.showinfo("Success", f"{self.animal_type} information saved!", parent=self)

        # Closing the window
        self.destroy()
