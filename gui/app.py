import tkinter as tk
import tkinter.ttk as ttk
import sv_ttk
from data.data_manager import load_animals, save_animals
from gui.animal_form import AnimalFormWindow

# Class that houses the main application framework and logic
class AnimalApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.load_all = None
        self.animal_type = None
        self.toggle_reserved_button = None
        self.selected_animal_name = None
        self.available_button = None
        self.sorting_frame = None
        self.load_button_dogs = None
        self.load_button_monkey = None
        self.add_button_dog = None
        self.add_button_monkey = None
        self.action_frame = None
        self.tree = None

        # Table column headers
        self.columns = ["Name", "Type", "Breed/Species", "Gender", "Age", "Weight", "Acquisition Date",
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

        reserved_status = value[9]

        # Debug print to check the values from Treeview
        print(f"Current reserved status: {reserved_status}")

        new_status = "Yes" if reserved_status == "No" else "No"

        # Debug print to check the values from Treeview
        print(f"New reserved status: {new_status}")

        # Setting the updated value and refreshing the treeview
        updated_values = value[:9] + [new_status] + value[10:]
        self.tree.item(selected_animal[0], values=updated_values)

        # Getting the animal name/type from the treeview
        animal_name = value[0]
        animal_type = value[1]

        # Debug print
        print(f"Looking for animal with name: {animal_name} and type: {animal_type}")

        # Load the correct file based on the selected animal type
        if animal_type == "Dog":
            file_name = "data/animal_data_dog.json"
        elif animal_type == "Monkey":
            file_name = "data/animal_data_monkey.json"
        else:
            tk.messagebox.showerror("Error", "Unknown animal type")
            return

        animals = load_animals(file_name)
        # Debug to check if animals are loaded
        print(f"Loaded {len(animals)} animals from {file_name}")

        # Find the selected animal by matching both name and type
        animal_found = False
        for animal in animals:
            # Debug to check if we are matching the correct animal
            print(f"Checking animal: {animal['name']} of type {animal['animal_type']}")
            # Matching the animal_name and animal_type, then applying the new updated status
            if animal["name"] == animal_name and animal["animal_type"] == animal_type:
                animal["reserved"] = new_status
                animal_found = True
                break
        # Error message if not found
        if not animal_found:
            tk.messagebox.showerror("Error", "Animal not found")
            return

        # Save the updated data back to the JSON file
        save_animals(file_name, animals)
        # Display to show success
        tk.messagebox.showinfo("Success", "Animal data saved")

    # All buttons to perform the actions
    def action_buttons(self):
        self.action_frame = ttk.LabelFrame(self.main_frame, text="Action")
        self.action_frame.grid(row=1, column=0, sticky="nw", padx=10, pady=0)

        self.load_button_dogs = ttk.Button(self.action_frame, text="Load Dogs", command=self.load_dogs)
        self.load_button_dogs.grid(row=0, column=0, padx=5, pady=5)

        self.load_button_monkey = ttk.Button(self.action_frame, text="Load Monkey", command=self.load_monkey)
        self.load_button_monkey.grid(row=1, column=0, padx=5, pady=5)

        self.load_all = ttk.Button(self.action_frame, text="Load All", command=self.load_all_animals)
        self.load_all.grid(row=2, column=0, padx=5, pady=5)

        self.add_button_dog = ttk.Button(self.action_frame, text="Add Dog", command=self.add_dog)
        self.add_button_dog.grid(row=3, column=0, padx=5, pady=5)

        self.add_button_monkey = ttk.Button(self.action_frame, text="Add Monkey", command=self.add_monkey)
        self.add_button_monkey.grid(row=4, column=0, padx=5, pady=5)

        self.available_button = ttk.Button(self.action_frame, text="Available", command=self.show_reserved)
        self.available_button.grid(row=0, column=2, padx=25, pady=5)

        self.toggle_reserved_button = ttk.Button(self.action_frame, text="Toggle Reserved", command=self.toggle_status)
        self.toggle_reserved_button.grid(row=0, column=3, padx=25, pady=5)

    # Load the Dogs from the JSON
    def load_dogs(self):
        dogs = load_animals("data/animal_data_dog.json")
        self.display_animals(dogs)

    # Load the Monkeys from the JSON
    def load_monkey(self):
        monkey = load_animals("data/animal_data_monkey.json")
        self.display_animals(monkey)

    # Loading all the animals to display
    def load_all_animals(self):
        print("Loading all animals")
        dogs = load_animals("data/animal_data_dog.json")
        monkey = load_animals("data/animal_data_monkey.json")

        all_animals = dogs + monkey
        print(f"Loaded animals: {all_animals}")
        self.display_animals(all_animals)

    # Calling the animal_form to add the animal, while passing in animal_type to make sure correct form is displayed
    def add_dog(self):
        AnimalFormWindow(self, animal_type="Dog")

    # Calling the animal_form to add the animal, while passing in animal_type to make sure correct form is displayed
    def add_monkey(self):
        AnimalFormWindow(self, animal_type="Monkey")

    # Function to make sure the animals are displayed properly in the treeview
    def display_animals(self, animals):

        for row in self.tree.get_children():
            self.tree.delete(row)

        for animal in animals:
            self.tree.insert("", "end", values=(
                animal.get("name"),
                animal.get("animal_type"),
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
        dogs = load_animals("data/animal_data_dog.json")
        monkey = load_animals("data/animal_data_monkey.json")

        all_animals = dogs + monkey
        reserved_animals = [animal for animal in all_animals if animal.get("reserved") == "No"]

        self.display_animals(reserved_animals)





