from data.database_manager import AnimalDatabase
import json


db = AnimalDatabase()

def insert_sample_data():
    if db.collection.count_documents({}) == 0:
        print("Inserting sample data")

        try:
            with open("data/sample_data.json", "r", encoding="utf-8") as file:
                sample_data = json.load(file)

            for animal in sample_data:
                db.collection.insert_one(animal)
            print("Inserted sample data")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Sample data already exists")

