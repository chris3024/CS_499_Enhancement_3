"""
gui.user_form
Handles the creation of new users
"""
import secrets
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from data.database_manager import AnimalDatabase

class CreateUserWindow(tk.Toplevel):
    """
    Class that handles the creation of new users
    """
    def __init__(self, parent):
        super().__init__(parent)

        self.db = AnimalDatabase()

        self.title("Create User")
        self.geometry("400x300")
        self.resizable(False, False)

        # User fields
        self.username_entry = ttk.Entry(self, width=30)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        ttk.Label(self, text="Username:").grid(row=0, column=0, padx=10, pady=10)

        self.password_entry = ttk.Entry(self, width=30, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        ttk.Label(self, text="Password:").grid(row=1, column=0, padx=10, pady=10)

        self.role_combobox = ttk.Combobox(self, values=["user", "admin"], state="readonly", width=28)
        self.role_combobox.set("user")
        self.role_combobox.grid(row=2, column=1, padx=10, pady=10)
        ttk.Label(self, text="Role:").grid(row=2, column=0, padx=10, pady=10)

        # Submit button
        self.submit_button = ttk.Button(self, text="Create User", command=self.create_user)
        self.submit_button.grid(row=3, column=0, columnspan=2, pady=10)

    # Gets the information and passes to method in database to create
    def create_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_combobox.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty.", parent=self)
            return

        # Call the create_user function from AnimalDatabase
        try:
            self.db.create_user(username, password or secrets.token_urlsafe(12), role)
            messagebox.showinfo("Success", "User created successfully.", parent=self)
            self.destroy()
        except ValueError as err:
            messagebox.showerror("Error", str(err), parent=self)
