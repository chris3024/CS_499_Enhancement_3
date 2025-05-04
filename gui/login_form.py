"""
gui.login_form
Handles the user login
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class LoginForm(tk.Toplevel):
    def __init__(self, parent, authenticate_callback, db):
        super().__init__(parent)

        self.db = db
        self.authenticate_callback = authenticate_callback

        self.title("Login")
        self.geometry("300x200")
        self.resizable(False, False)

        # Username and Password Fields
        ttk.Label(self, text="Username:").grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self, text="Password:").grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Login Button
        self.login_button = ttk.Button(self, text="Login", command=self.authenticate)
        self.login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    # compares entry to database information
    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Authenticate user using the database method
        user, is_first_login = self.db.authenticate_user(username, password)

        if user:
            messagebox.showinfo("Success", "Login Successful!")
            self.authenticate_callback(user, is_first_login)  # Callback to mark login as successful
            self.destroy()  # Close the login window
        else:
            messagebox.showerror("Error", "Invalid username or password.")
