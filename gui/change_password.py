"""
gui.change_password
Handles the changing of the password on first login
"""

import bcrypt
import tkinter as tk
from tkinter import ttk, messagebox
from pymongo.errors import PyMongoError
from data.database_manager import AnimalDatabase


class ChangePasswordWindow(tk.Toplevel):
    """
    Prompts user to set a new password on first login.
    """

    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        self.db = AnimalDatabase()

        self.title("Change Password")
        self.geometry("400x200")
        self.resizable(False, False)

        self._build_ui()

    def _build_ui(self):
        form_frame = ttk.Frame(self)
        form_frame.pack(padx=20, pady=20)

        ttk.Label(form_frame, text="New Password:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.new_password_entry = ttk.Entry(form_frame, width=30, show="*")
        self.new_password_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Confirm Password:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.confirm_password_entry = ttk.Entry(form_frame, width=30, show="*")
        self.confirm_password_entry.grid(row=1, column=1, padx=5, pady=5)

        submit_btn = ttk.Button(self, text="Change Password", command=self._change_password)
        submit_btn.pack(pady=10)

    def _change_password(self):
        password = self.new_password_entry.get()
        confirm = self.confirm_password_entry.get()

        if password != confirm:
            messagebox.showerror("Mismatch", "Passwords do not match.", parent=self)
            return

        if len(password) < 6:
            messagebox.showwarning("Weak Password", "Password must be at least 6 characters.", parent=self)
            return

        try:
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            self.db.users.update_one(
                {"_id": self.user["_id"]},
                {"$set": {"password": hashed, "is_first_login": False}}
            )
            messagebox.showinfo("Success", "Password changed successfully.", parent=self)
            self.destroy()
        except PyMongoError as e:
            messagebox.showerror("Database Error", f"Could not update password: {e}", parent=self)
