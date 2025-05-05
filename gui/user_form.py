"""
gui.user_form
Handles the creation of new users
"""

import secrets
import tkinter as tk
from tkinter import ttk, messagebox
from data.database_manager import AnimalDatabase

class CreateUserWindow(tk.Toplevel):
    """
    Window for creating new user accounts (admin or regular).
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.db = AnimalDatabase()

        self.title("Create User")
        self.geometry("360x220")
        self.resizable(False, False)

        self._build_ui()

    def _build_ui(self):
        frame = ttk.Frame(self)
        frame.pack(padx=20, pady=20)

        # Username
        ttk.Label(frame, text="Username:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.username_entry = ttk.Entry(frame, width=30)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        # Password
        ttk.Label(frame, text="Password:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.password_entry = ttk.Entry(frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Role
        ttk.Label(frame, text="Role:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.role_combobox = ttk.Combobox(frame, values=["user", "admin"], state="readonly", width=28)
        self.role_combobox.set("user")
        self.role_combobox.grid(row=2, column=1, padx=5, pady=5)

        # Submit
        submit_btn = ttk.Button(self, text="Create User", command=self._create_user)
        submit_btn.pack(pady=10)

    def _create_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_combobox.get()

        if not username:
            messagebox.showerror("Input Error", "Username is required.", parent=self)
            return

        try:
            self.db.create_user(username, password or secrets.token_urlsafe(12), role)
            messagebox.showinfo("Success", f"User '{username}' created successfully.", parent=self)
            self.destroy()
        except ValueError as err:
            messagebox.showerror("Error", str(err), parent=self)
