"""
data.database_manager
Handles the database tasks and connections
"""
import os, logging, bcrypt
from pymongo import MongoClient, errors
from bson.objectid import ObjectId


class AnimalDatabase:
    def __init__(self, mongo_uri: str | None = None,
                 database="rescue_animals_db", collection="animals", user_collection="users"):
        mongo_uri = mongo_uri or os.environ.get("MONGO_URI", "mongodb://localhost:27017")
        self._database = database
        self._collection = collection
        self._user_collection = user_collection

        try:
            # Connecting to local database immediately when initializing the class
            self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
            self.client.admin.command('ping')
            self.db = self.client[self._database]
            self.collection = self.db[self._collection]
            self.users_collection = self.db[self._user_collection]

            # Debug statement
            logging.info("Connected to MongoDB %s", database)

            # Adding default admin on first run
            if self.users_collection.count_documents({}) == 0:
                print("No users found....Creating default user")
                default_pwd = os.getenv("ADMIN_PASSWORD", "admin1234")
                self.create_user("admin", default_pwd, "admin")

        except errors.ConnectionFailure as e:
            logging.error("Error connecting to MongoDB: %s", e)

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


