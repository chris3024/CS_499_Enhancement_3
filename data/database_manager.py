from pymongo import MongoClient
from bson.objectid import ObjectId
import hashlib

class AnimalDatabase:
    def __init__(self, host="localhost", port=27017, database="rescue_animals_db", collection="animals",
                 user_collection="users"):
        self._host = host
        self._port = port
        self._database = database
        self._collection = collection
        self._user_collection = user_collection

        try:
            # Connecting to local database immediately when initializing the class
            self.client = MongoClient(host, port)
            self.db = self.client[self._database]
            self.collection = self.db[self._collection]
            self.users_collection = self.db[self._user_collection]

            # Debug statement
            print(f"connected to database {self._database}")

            # Adding default user on first run
            if self.users_collection.count_documents({}) == 0:
                print("No users found....Creating default user")
                self.create_user("admin", "admin1234", "admin")

        except ConnectionError as e:
            print(f"Error: {e}")
            raise

    # Used to check user role
    @staticmethod
    def is_admin(user):
        return user.get("role") == "admin"

    # User Authentication and Admin stuff
    def authenticate_user(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        user = self.users_collection.find_one({'username': username, "password": hashed_password})

        if user:
            if user.get("is_first_login", False):
                return user, True
            return user, False
        return None, False

    # Method for admin accounts to create new users
    def create_user(self, username, password, role="user"):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.users_collection.insert_one({
            "username": username,
            "password": hashed_password,
            "role": role,
            "is_first_login": True,
        })
        # Debug
        print(f"User {username} created with role {role}")

    # Creating and inserting the animal into the database
    def create_animal(self, animal_data):

        try:
            self.collection.insert_one(animal_data)
            print(f"Created new animal: {animal_data}")
        except Exception as e:
            print(f"Error: {e}")
            return False
        return True

    # Reading all animals
    def read_all_animals(self, query=None):
        try:
            query = query or {}
            cursor = self.collection.find(query)
            return [animal for animal in cursor]
        except Exception as e:
            print(f"Error: {e}")

    # Update animals
    def update_animal(self, animal_id, animal_name, updated_fields):

        try:
            result = self.collection.update_one({"_id": ObjectId(animal_id), "name": animal_name}, {"$set": updated_fields})
            if result.modified_count == 0:
                print(f"No updates made for {animal_name}")
                return False
            print(f"Updated {animal_name} with {updated_fields}")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    # Delete animal
    def delete_animal(self, animal_id, animal_name):

        try:
            result = self.collection.delete_one({"_id": ObjectId(animal_id), "name": animal_name})
            if result.deleted_count == 0:
                print(f"No deletes made for {animal_name}")
                return False
            print(f"Deleted {animal_name} with {result.deleted_count}")
            return True
        except Exception as e:
            print(f"Error: {e}")


