"""
gui.app
Handles the creation and display of the main application window
Also, houses the functions for the actions to make the dashboard interactive
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk

from data.database_manager import AnimalDatabase
from gui.animal_form import AnimalFormWindow
from gui.login_form import LoginForm
from gui.change_password import ChangePasswordWindow
from gui.user_form import CreateUserWindow


class AnimalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.db = AnimalDatabase()
        self.logged_in = False
        self.user_role = None

        self.columns = [
            "Name", "Type", "Breed/Species", "Gender", "Age", "Weight",
            "Acquisition Date", "Acquisition Country", "Training Status",
            "Reserved", "In Service Country"
        ]

        self.title("Grazioso Salvare Animal Rescue Operations")
        self.geometry("1090x600")
        self.resizable(False, False)
        sv_ttk.set_theme('light')

        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(column=0, row=0, sticky="nw", padx=0, pady=10)

        self.tree = None
        self.action_frame = None
        self._setup_ui()

    def _setup_ui(self):
        self._create_table()
        self._create_action_buttons()

    def _create_table(self):
        column_widths = {
            "Name": 100, "Type": 80, "Breed/Species": 150, "Gender": 80, "Age": 50,
            "Weight": 60, "Acquisition Date": 110, "Acquisition Country": 120,
            "Training Status": 120, "Reserved": 70, "In Service Country": 120
        }

        self.tree = ttk.Treeview(self.main_frame, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 100), anchor="center", stretch=False)
        self.tree.grid(column=0, row=0, sticky="nsew", padx=10, pady=10)

    def _create_action_buttons(self):
        self.action_frame = ttk.LabelFrame(self.main_frame, text="Actions")
        self.action_frame.grid(row=1, column=0, sticky="nw", padx=10, pady=0)

        actions = [
            ("Login", self.check_login, 0, 0),
            ("Create User", self.create_user, 1, 0),
            ("Load Dogs", self.load_dogs, 0, 2),
            ("Load Monkey", self.load_monkey, 1, 2),
            ("Load All", self.load_all_animals, 2, 2),
            ("Add Dog", self.add_dog, 0, 3),
            ("Add Monkey", self.add_monkey, 1, 3),
            ("Delete Animal", self.delete_animal, 0, 4),
            ("Available", self.show_available, 0, 6),
            ("Toggle Reserved", self.toggle_reserved_status, 1, 6)
        ]

        self.buttons = {}
        for text, command, row, col in actions:
            btn = ttk.Button(self.action_frame, text=text, command=command)
            btn.grid(row=row, column=col, padx=15, pady=5)
            self.buttons[text] = btn

        self.buttons["Create User"].grid_remove()  # Hidden until admin logs in

    def check_login(self):
        if not self.logged_in:
            LoginForm(self, self.on_login_success, self.db)

    def on_login_success(self, user, is_first_login=False):
        self.logged_in = True
        self.user_role = user["role"]
        if is_first_login:
            self.open_change_password(user)
        if self.db.is_admin(user):
            self.buttons["Create User"].grid()

    def open_change_password(self, user):
        ChangePasswordWindow(self, user)

    def _require_login(self) -> bool:
        if not self.logged_in:
            messagebox.showwarning("Login Required", "Please log in first.")
            return False
        return True

    def create_user(self):
        CreateUserWindow(self)

    def load_animals(self, query=None):
        if not self._require_login():
            return
        animals = self.db.read_all_animals(query)
        self.display_animals(animals)

    def load_dogs(self):
        self.load_animals({"animal_type": "Dog"})

    def load_monkey(self):
        self.load_animals({"animal_type": "Monkey"})

    def load_all_animals(self):
        self.load_animals()

    def add_dog(self):
        if self._require_login():
            AnimalFormWindow(self, animal_type="Dog")

    def add_monkey(self):
        if self._require_login():
            AnimalFormWindow(self, animal_type="Monkey")

    def delete_animal(self):
        if not self._require_login():
            return

        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "No animal selected")
            return

        animal_id = selected[0]
        if self.db.delete_animal(animal_id):
            self.tree.delete(animal_id)
            messagebox.showinfo("Deleted", "Animal record removed.")
        else:
            messagebox.showerror("Error", "Animal could not be deleted.")

    def display_animals(self, animals):
        if not animals:
            messagebox.showerror("Error", "No animals found.")
            return

        self.tree.delete(*self.tree.get_children())

        for animal in animals:
            self.tree.insert(
                "", "end", iid=str(animal["_id"]),
                values=(
                    animal["name"],
                    animal.get("animal_type", ""),
                    animal.get("breed") or animal.get("species", ""),
                    animal.get("gender", ""),
                    animal.get("age", ""),
                    animal.get("weight", ""),
                    animal.get("acquisition_date", "")[:10],
                    animal.get("acquisition_country", ""),
                    animal.get("training_status", ""),
                    "Yes" if animal.get("reserved") else "No",
                    animal.get("in_service_country", "")
                )
            )

    def show_available(self):
        if self._require_login():
            self.load_animals({"animal_type": {"$in": ["Dog", "Monkey"]}, "reserved": False})

    def toggle_reserved_status(self):
        if not self._require_login():
            return

        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "No animal selected")
            return

        animal_id = selected[0]
        current_status = self.tree.set(animal_id, "Reserved")
        new_status = current_status == "No"
        if self.db.update_animal(animal_id, {"reserved": new_status}):
            self.tree.set(animal_id, "Reserved", "Yes" if new_status else "No")
            messagebox.showinfo("Updated", f"Animal {animal_id} reservation status toggled.")
        else:
            messagebox.showerror("Error", "Failed to update reservation status.")
