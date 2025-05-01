# main.py

from gui.app import AnimalApp
import sample_data

if __name__ == '__main__':
    # loading sample data
    sample_data.insert_sample_data()

    # Application start
    app = AnimalApp()
    app.mainloop()