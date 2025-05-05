from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

from animals.dog import Dog
from animals.monkey import Monkey


class AnimalFormWindow(tk.Toplevel):
    """
    A dynamic form for creating Dog or Monkey records in the database.
    """

    def __init__(self, parent, animal_type: str):
        super().__init__(parent)
        self.db = parent.db
        self.animal_type = animal_type
        self.inputs = {}

        self.title(f"Add {animal_type}")
        self.geometry("400x600")
        self.resizable(False, False)

        self._build_form()

    def _build_form(self):
        field_width = 30
        frame = ttk.LabelFrame(self, text="Add Animal")
        frame.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")

        def add_input(label, row, widget_function):
            ttk.Label(frame, text=label).grid(column=0, row=row, padx=10, pady=5, sticky="e")
            widget = widget_function()
            widget.grid(column=1, row=row, padx=10, pady=5, sticky="w")
            self.inputs[label.lower().replace(" ", "_")] = widget

        add_input("Name", 0, lambda: ttk.Entry(frame, width=field_width))

        if self.animal_type == "Dog":
            add_input("Breed", 1, lambda: ttk.Entry(frame, width=field_width))
        else:
            add_input("Species", 1, lambda: ttk.Combobox(
                frame, values=["Capuchin", "Guenon", "Macaque", "Marmoset", "Squirrel Monkey", "Tamarin"],
                state="readonly", width=25))

        add_input("Gender", 2, lambda: ttk.Combobox(
            frame, values=["Male", "Female"], state="readonly", width=25))

        for label, row in [("Age", 3), ("Weight", 4)]:
            add_input(label, row, lambda: ttk.Entry(
                frame, width=field_width,
                validate="key",
                validatecommand=(self.register(self._validate_integer), "%P")
            ))

        add_input("Acquisition Date", 5, lambda: ttk.Entry(frame, width=field_width))
        self.inputs["acquisition_date"].insert(0, datetime.today().strftime('%Y-%m-%d'))

        add_input("Acquisition Country", 6, lambda: ttk.Entry(frame, width=field_width))
        add_input("Training Status", 7, lambda: ttk.Combobox(
            frame, values=["Not Trained", "In Training", "Fully Trained"], state="readonly", width=25))
        add_input("Reserved", 8, lambda: ttk.Combobox(
            frame, values=["Yes", "No"], state="readonly", width=25))
        self.inputs["reserved"].set("No")

        add_input("In Service Country", 9, lambda: ttk.Entry(frame, width=field_width))

        submit_btn = ttk.Button(frame, text="Submit", command=self._submit_form)
        submit_btn.grid(row=10, column=1, padx=10, pady=10, sticky="e")

    @staticmethod
    def _validate_integer(value: str) -> bool:
        return value.isdigit() or value == ""

    def _validate_integer_wrapper(self, value: str) -> int:
        return self._validate_integer(value)

    def _submit_form(self):
        try:
            name = self.inputs["name"].get().strip()
            age = int(self.inputs["age"].get())
            weight = float(self.inputs["weight"].get())
            gender = self.inputs["gender"].get()
            acquisition_country = self.inputs["acquisition_country"].get().strip()
            training_status = self.inputs["training_status"].get()
            reserved = self.inputs["reserved"].get() == "Yes"
            in_service_country = self.inputs["in_service_country"].get().strip()

            if not all([name, gender, acquisition_country, training_status, in_service_country]):
                raise ValueError("All required fields must be filled.")

            extra_key = "breed" if self.animal_type == "Dog" else "species"
            extra_value = self.inputs[extra_key].get().strip()
            if not extra_value:
                raise ValueError(f"{extra_key.capitalize()} is required.")

            common_data = {
                "name": name,
                "gender": gender,
                "age": age,
                "weight": weight,
                "acquisition_country": acquisition_country,
                "training_status": training_status,
                "reserved": reserved,
                "in_service_country": in_service_country,
            }

            animal_class = Dog if self.animal_type == "Dog" else Monkey
            animal = animal_class(**common_data, **{extra_key: extra_value})

            if self.db.create_animal(animal.to_dict()):
                messagebox.showinfo("Success", f"{self.animal_type} saved successfully!", parent=self)
                self.destroy()

        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve), parent=self)
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An error occurred: {e}", parent=self)
