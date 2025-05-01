# data/data_manager.py

import json

def load_animals(file_name):
    # Loading dogs from JSON
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            animals = json.load(file)
        print(f"Loaded animals: {animals}")
        return animals
    except FileNotFoundError:
        print(f"{file_name} not found!")
        return []

def save_animals(file_name, animal_data):
    # Saving the data to the JSON
    try:

        if isinstance(animal_data, list) and all(isinstance(item, dict) for item in animal_data):
            with open(file_name, "w", encoding="utf-8") as file:
                json.dump(animal_data, file, indent=4)
            print(f"Data saved to {file_name} successfully!")
        else:
            print("Error: animal_data must be a list of dictionaries.")
    except Exception as e:
        print(f"Error saving data to {file_name}: {e}")
