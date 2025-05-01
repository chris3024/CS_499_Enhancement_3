# gui/change_password.py

import hashlib
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from data.database_manager import AnimalDatabase

class ChangePasswordWindow(tk.Toplevel):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        self.db = AnimalDatabase()

        self.title("Change Password")
        self.geometry("400x300")
        self.resizable(False, False)

        # Labels and Entries for New Password
        ttk.Label(self, text="New Password:").grid(row=0, column=0, padx=10, pady=10)
        self.new_password_entry = ttk.Entry(self, width=30, show="*")
        self.new_password_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self, text="Confirm Password:").grid(row=1, column=0, padx=10, pady=10)
        self.confirm_password_entry = ttk.Entry(self, width=30, show="*")
        self.confirm_password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Submit button
        self.submit_button = ttk.Button(self, text="Change Password", command=self.change_password)
        self.submit_button.grid(row=2, column=0, columnspan=2, pady=10)

    def change_password(self):
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.", parent=self)
            return

        # Hash the new password
        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

        # Update the password in the database
        try:
            self.db.users_collection.update_one(
                {"_id": self.user["_id"]},
                {"$set": {"password": hashed_password, "is_first_login": False}}  # Set is_first_login to False
            )
            messagebox.showinfo("Success", "Password changed successfully.", parent=self)
            self.destroy()  # Close the change password window
        except Exception as e:
            messagebox.showerror("Error", f"Failed to change password: {e}", parent=self)
