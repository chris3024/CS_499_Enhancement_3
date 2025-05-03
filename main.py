# main.py

from __future__ import annotations
import logging
import sys

# Configuring logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logging.info("Starting")

from tkinter import Tk, ttk
from gui.app import AnimalApp



def main() -> None:




    try:
        app = AnimalApp()
        app.mainloop()
    except RuntimeError as err:
        logging.error("Application failed to start: %s", err, exc_info=True)
        root = Tk()
        root.withdraw()
        ttk.messagebox.showerror("Database error", str(err))
        root.destroy()

if __name__ == '__main__':
     main()