"""
gui.app
Handles the creation and display of the main application window
Also, houses the functions for the actions to make the dashboard interactive
"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import sv_ttk
from data.database_manager import AnimalDatabase
from gui.animal_form import AnimalFormWindow
from gui.login_form import LoginForm
from gui.change_password import ChangePasswordWindow
from gui.user_form import CreateUserWindow


# Class that houses the main application framework and logic
class AnimalApp(tk.Tk):
    def __init__(self):
        super().__init__()


        self.db = AnimalDatabase()
        self.logged_in = False
        self.user_role = None

        self.create_user_button = None
        self.delete_button = None
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
        self.columns = ["Name", "Type", "Breed/Species", "Gender", "Age", "Weight", "Acquisition Date",
                        "Acquisition Country", "Training Status", "Reserved", "In Service Country"]

        self.title("Grazioso Salvare Animal Rescue Operations")
        self.geometry("1090x600")
        self.resizable(width=False, height=False)
        sv_ttk.set_theme('light')

        # Main Frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(column=0, row=0, sticky="nw", padx=0, pady=10)

        self.create_table()
        self.action_buttons()

    # Login to access data
    def check_login(self):
        if not self.logged_in:
            LoginForm(self, self.on_login_success, self.db)

    # Check for login success
    def on_login_success(self, user, is_first_login=False):
        self.logged_in = True
        self.user_role = user["role"]

        if is_first_login:
            self.open_change_password(user)

        if self.db.is_admin(user):
            self.create_user_button.grid(row=0, column=1, padx=25, pady=5)

    # Window to change password after first login
    def open_change_password(self, user):
        ChangePasswordWindow(self, user)


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


    # All buttons to perform the actions
    def action_buttons(self):
        self.action_frame = ttk.LabelFrame(self.main_frame, text="Action")
        self.action_frame.grid(row=1, column=0, sticky="nw", padx=10, pady=0)

        self.load_button_dogs = ttk.Button(self.action_frame, text="Load Dogs", command=self.load_dogs)
        self.load_button_dogs.grid(row=0, column=2, padx=15, pady=5)

        self.load_button_monkey = ttk.Button(self.action_frame, text="Load Monkey", command=self.load_monkey)
        self.load_button_monkey.grid(row=1, column=2, padx=15, pady=5)

        self.load_all = ttk.Button(self.action_frame, text="Load All", command=self.load_all_animals)
        self.load_all.grid(row=2, column=2, padx=15, pady=5)

        self.add_button_dog = ttk.Button(self.action_frame, text="Add Dog", command=self.add_dog)
        self.add_button_dog.grid(row=0, column=3, padx=15, pady=5)

        self.add_button_monkey = ttk.Button(self.action_frame, text="Add Monkey", command=self.add_monkey)
        self.add_button_monkey.grid(row=1, column=3, padx=15, pady=5)

        self.available_button = ttk.Button(self.action_frame, text="Available", command=self.show_reserved)
        self.available_button.grid(row=0, column=6, padx=25, pady=5)

        self.toggle_reserved_button = ttk.Button(self.action_frame, text="Toggle Reserved", command=self.toggle_status)
        self.toggle_reserved_button.grid(row=1, column=6, padx=25, pady=5)

        self.delete_button = ttk.Button(self.action_frame, text="Delete Animal", command=self.delete_animal)
        self.delete_button.grid(row=0, column=4, padx=25, pady=5)



        self.login_button = ttk.Button(self.action_frame, text="Login", command=self.check_login)
        self.login_button.grid(row=0, column=0, padx=25, pady=5)

        self.create_user_button = ttk.Button(self.action_frame, text="Create User", command=self.create_user)
        self.create_user_button.grid(row=1, column=0, padx=25, pady=5)
        self.create_user_button.grid_forget()

    # Calls new window to create user
    def create_user(self):
        CreateUserWindow(self)

    # Load the Dogs from the database
    def load_dogs(self):

        # Checking logged in
        if not self.logged_in:
            tk.messagebox.showwarning("Login Required", "You must login first.")
            return

        # Searching through the database looking for type == Dog
        query = {"animal_type": "Dog"}
        #print("DEBUG‑load_dogs query →", query)

        animals = self.db.read_all_animals(query)
        #print("DEBUG‑load_dogs result →", animals)

        self.display_animals(animals)

    # Load the Monkeys from the database
    def load_monkey(self):

        # Checking logged in
        if not self.logged_in:
            tk.messagebox.showwarning("Login Required", "You must login first.")
            return

        # Searching through the database looking for type == Monkey
        query = {"animal_type": "Monkey"}
        animals = self.db.read_all_animals(query)

        self.display_animals(animals)

    # Loading all the animals to display
    def load_all_animals(self):

        # Checking logged in
        if not self.logged_in:
            tk.messagebox.showwarning("Login Required", "You must login first.")
            return

        #print("Loading all animals")
        animals = self.db.read_all_animals()

        self.display_animals(animals)

    # Calling the animal_form to add the animal, while passing in animal_type to make sure correct form is displayed
    def add_dog(self):

        # Checking logged in
        if not self.logged_in:
            tk.messagebox.showwarning("Login Required", "You must login first.")
            return

        AnimalFormWindow(self, animal_type="Dog")

    # Calling the animal_form to add the animal, while passing in animal_type to make sure correct form is displayed
    def add_monkey(self):

        # Checking logged in
        if not self.logged_in:
            tk.messagebox.showwarning("Login Required", "You must login first.")
            return

        AnimalFormWindow(self, animal_type="Monkey")

    # Retrieve the animal from the treeview, then passing _id to delete the animal
    def delete_animal(self):

        # Checking logged in
        if not self.logged_in:
            tk.messagebox.showwarning("Login Required", "You must login first.")
            return

        # Getting the selected animal from the treeview
        selected_animal = self.tree.selection()

        # Error checking to make sure animal is selected
        if not selected_animal:
            tk.messagebox.showerror("Error", "No animal selected")
            return

        mongo_id = selected_animal[0]

        # Debug print to check the values from Treeview
        #print(f"Selected animal: {mongo_id}")

        # Calling CRUD method to delete animal from database and update treeview
        if self.db.delete_animal(mongo_id):
            self.tree.delete(mongo_id)
            tk.messagebox.showinfo("Success", "Animal deleted")
        else:
            tk.messagebox.showerror("Error", "Animal not found")

    # Function to make sure the animals are displayed properly in the treeview
    def display_animals(self, animals):

        #print("DEBUG - animals: ", animals)
        if not animals:
            tk.messagebox.showerror("Error", "No animals found")
            return

        if isinstance(animals, dict):
            animals = [animals]

        for row in self.tree.get_children():
            self.tree.delete(row)


        for animal in animals:
            reserved_str = "Yes" if animal.get("reserved") else "No"
            acq_raw = animal.get("acquisition_date")
            acquisition_date = animal["acquisition_date"][:10] if acq_raw else "-"

            self.tree.insert(
                "",
                "end",
                iid=str(animal["_id"]),
                values=(
                    animal["name"],
                    animal["animal_type"],
                    animal.get("breed", animal.get("species", "")),
                    animal["gender"],
                    animal["age"],
                    animal["weight"],
                    acquisition_date,
                    animal["acquisition_country"],
                    animal["training_status"],
                    reserved_str,
                    animal["in_service_country"],
                ),
            )

    # Function to filter the animals to show animals with a reserved status
    def show_reserved(self):

        # Checking logged in
        if not self.logged_in:
            tk.messagebox.showwarning("Login Required", "You must login first.")
            return

        query = {"animal_type": {"$in": ["Dog", "Monkey"]}, "reserved": False}

        animals = self.db.read_all_animals(query)

        self.display_animals(animals)

    # Function to toggle reserved_status
    def toggle_status(self):

        # Checking logged in
        if not self.logged_in:
            tk.messagebox.showwarning("Login Required", "You must login first.")
            return

        # Getting the selected animal from the treeview
        selected_animal = self.tree.selection()

        # Error checking to make sure animal is selected
        if not selected_animal:
            tk.messagebox.showerror("Error", "No animal selected")
            return

        iid = selected_animal[0]

        current = self.tree.set(iid, "Reserved")
        new_reserved_bool = current == "No"
        new_reserved_text = "Yes" if new_reserved_bool else "No"

        if self.db.update_animal(iid, {"reserved": new_reserved_bool}):
            self.tree.set(iid, "Reserved", new_reserved_text)
            tk.messagebox.showinfo("Success", f"Animal {iid} updated.")
        else:
            tk.messagebox.showerror("Error", f"Animal {iid} could not be updated.")





