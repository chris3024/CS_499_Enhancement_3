"""
main
Starting point of application
"""

from __future__ import annotations
import logging
import sys
from tkinter import Tk, messagebox
from gui.app import AnimalApp

# Configuring logger to display
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logging.info("Starting")

def main() -> None:
    """
    Main function to start the application.
    Includes logging for errors
    :return:
    """
    try:
        app = AnimalApp()
        app.mainloop()
    except RuntimeError as err:
        logging.error("Application failed to start: %s", err, exc_info=True)
        root = Tk()
        root.withdraw()
        messagebox.showerror("Database error", str(err))
        root.destroy()

if __name__ == '__main__':
    main()
