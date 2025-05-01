import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import sv_ttk
from data.database_manager import AnimalDatabase


# Class that houses the main application framework and logic
class AnimalApp(tk.Tk):
    def __init__(self):
        super().__init__()


        self.db = AnimalDatabase()

        self.login_button = None
        self.load_all = None
        self.animal_type = None
        self.toggle_reserved_button = None
        self.selected_animal_name = None
        self.available_button = None
        self.load_button_dogs = None
        self.load_button_monkey = None
        self.add_button_dog = None
        self.add_button_monkey = None
        self.action_frame = None
        self.tree = None

        # Table column headers
        self.columns = ["_id", "Name", "Type", "Breed/Species", "Gender", "Age", "Weight", "Acquisition Date",
                        "Acquisition Country", "Training Status", "Reserved", "In Service Country"]

        self.title("Grazioso Salvare Animal Rescue Operations")
        self.geometry("1090x600")
        self.resizable(width=False, height=False)
        sv_ttk.set_theme('light')

        # Main Frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(column=0, row=0, sticky="nw", padx=0, pady=10)

        # Main Frame configuration
        self.main_frame.columnconfigure(0, weight=1, uniform="equal")
        self.main_frame.columnconfigure(1, weight=0, uniform="equal")
        self.main_frame.rowconfigure(0, weight=1, uniform="equal")
        self.main_frame.rowconfigure(1, weight=0)

        self.create_table()
        self.action_buttons()

    # Creates the table that holds the animal data to display
    def create_table(self):
        column_widths = {
            "_id": 0,
            "Name": 100,
            "Type": 80,
            "Breed/Species": 150,
            "Gender": 80,
            "Age": 50,
            "Weight": 60,
            "Acquisition Date": 110,
            "Acquisition Country": 120,
            "Training Status": 120,
            "Reserved": 70,
            "In Service Country": 120
        }

        self.tree = ttk.Treeview(self.main_frame, columns=self.columns, show="headings")

        for column in self.columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=column_widths.get(column, 100), anchor="center", stretch=False)

        self.tree.grid(column=0, row=0, sticky="nsew", padx=10, pady=10)

    # Function to toggle reserved_status
    def toggle_status(self):

        # Getting the selected animal from the treeview
        selected_animal = self.tree.selection()

        # Error checking to make sure animal is selected
        if not selected_animal:
            tk.messagebox.showerror("Error", "No animal selected")
            return

        # Getting the selected animals information
        item = self.tree.item(selected_animal[0])
        value = item['values']

        # Debug print to check the values from Treeview
        print(f"Selected animal: {value}")

        # Getting the animal ID
        animal_id = value[0]

        # Getting the reserved status
        reserved_status = value[10]

        # Setting new reserved status
        new_status = "Yes" if reserved_status == "No" else "No"

        updated_values = value[:10] + [new_status] + value[11:]
        self.tree.item(selected_animal[0], values=updated_values)

        # query parameters and finding the animal
        updated_fields = {"reserved": new_status}

        if self.db.update_animal(animal_id, updated_fields):
            tk.messagebox.showinfo("Success", f"Animal {animal_id} updated.")
        else:
            tk.messagebox.showerror("Error", f"Animal {animal_id} could not be updated.")

    # All buttons to perform the actions
    def action_buttons(self):
        self.action_frame = ttk.LabelFrame(self.main_frame, text="Action")
        self.action_frame.grid(row=1, column=0, sticky="nw", padx=10, pady=0)

        self.load_button_dogs = ttk.Button(self.action_frame, text="Load Dogs", command=self.load_dogs)
        self.load_button_dogs.grid(row=0, column=2, padx=5, pady=5)

        self.load_button_monkey = ttk.Button(self.action_frame, text="Load Monkey", command=self.load_monkey)
        self.load_button_monkey.grid(row=1, column=2, padx=5, pady=5)

        self.load_all = ttk.Button(self.action_frame, text="Load All", command=self.load_all_animals)
        self.load_all.grid(row=2, column=2, padx=5, pady=5)

        self.add_button_dog = ttk.Button(self.action_frame, text="Add Dog")
        self.add_button_dog.grid(row=3, column=2, padx=5, pady=5)

        self.add_button_monkey = ttk.Button(self.action_frame, text="Add Monkey")
        self.add_button_monkey.grid(row=4, column=2, padx=5, pady=5)

        self.available_button = ttk.Button(self.action_frame, text="Available", command=self.show_reserved)
        self.available_button.grid(row=0, column=4, padx=25, pady=5)

        self.toggle_reserved_button = ttk.Button(self.action_frame, text="Toggle Reserved", command=self.toggle_status)
        self.toggle_reserved_button.grid(row=1, column=4, padx=25, pady=5)

#TODO: Add Delete and Add Login Functionality

        self.login_button = ttk.Button(self.action_frame, text="Login")
        self.login_button.grid(row=0, column=0, padx=25, pady=5)

    # Load the Dogs from the database
    def load_dogs(self):

        # Searching through the database looking for type == Dog
        query = {"type": "Dog"}
        animals = self.db.read_all_animals(query)

        self.display_animals(animals)

    # Load the Monkeys from the database
    def load_monkey(self):

        # Searching through the database looking for type == Monkey
        query = {"type": "Monkey"}
        animals = self.db.read_all_animals(query)

        self.display_animals(animals)

    # Loading all the animals to display
    def load_all_animals(self):
        print("Loading all animals")
        animals = self.db.read_all_animals()

        self.display_animals(animals)

#TODO:    # Calling the animal_form to add the animal, while passing in animal_type to make sure correct form is displayed
    # def add_dog(self):
    #     AnimalFormWindow(self, animal_type="Dog")
    #
    # # Calling the animal_form to add the animal, while passing in animal_type to make sure correct form is displayed
    # def add_monkey(self):
    #     AnimalFormWindow(self, animal_type="Monkey")

    # Function to make sure the animals are displayed properly in the treeview
    def display_animals(self, animals):

        for row in self.tree.get_children():
            self.tree.delete(row)

        for animal in animals:
            self.tree.insert("", "end", values=(
                animal.get("_id"),
                animal.get("name"),
                animal.get("type"),
                animal.get("breed") if "breed" in animal else animal.get("species"),
                animal.get("gender"),
                animal.get("age"),
                animal.get("weight"),
                animal.get("acquisition_date"),
                animal.get("acquisition_country"),
                animal.get("training_status"),
                animal.get("reserved"),
                animal.get("in_service_country"),
            ))

    # Function to filter the animals to show animals with a reserved status
    def show_reserved(self):
        query = {"type": {"$in": ["Dog", "Monkey"]}, "reserved": "Yes"}

        animals = self.db.read_all_animals(query)

        self.display_animals(animals)





