"""
gui.login_form
Handles the user login
"""

import tkinter as tk
from tkinter import ttk, messagebox


class LoginForm(tk.Toplevel):
    """
    Login window for authenticating users via the database.
    """

    def __init__(self, parent, authenticate_callback, db):
        super().__init__(parent)
        self.db = db
        self.authenticate_callback = authenticate_callback

        self.title("Login")
        self.geometry("300x180")
        self.resizable(False, False)

        self._build_ui()

    def _build_ui(self):
        frame = ttk.Frame(self)
        frame.pack(padx=20, pady=20)

        ttk.Label(frame, text="Username:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.username_entry = ttk.Entry(frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Password:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.password_entry = ttk.Entry(frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        login_btn = ttk.Button(self, text="Login", command=self._authenticate)
        login_btn.pack(pady=10)

    def _authenticate(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Missing Input", "Username and password are required.", parent=self)
            return

        user, is_first_login = self.db.authenticate_user(username, password)
        if user:
            messagebox.showinfo("Login Successful", f"Welcome, {username}!", parent=self)
            self.authenticate_callback(user, is_first_login)
            self.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.", parent=self)
