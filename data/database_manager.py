"""
data.database_manager
Handles the database tasks and connections
"""
import logging
import os
import bcrypt


from bson.objectid import ObjectId
from pymongo import MongoClient, errors


class AnimalDatabase:
    """
    Class to handle database functions, including:
    Database connections, role, authentication, creation of users,
    and the CRUD operations
    """

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
            logging.info("MONGO URI → %s", mongo_uri)
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

    # User Authentication
    def authenticate_user(self, username: str, password:str) -> tuple[dict | None, bool]:

        user = self.users_collection.find_one({"username": username})
        if user and bcrypt.checkpw(password.encode(), user["password"]):
            return user, bool(user.get("is_first_login"))
        return None, False

    # Method for admin accounts to create new users
    def create_user(self, username: str, password: str, role: str = "user", *, first_login: bool = True) -> None:
        if role not in ("user", "admin"):
            raise ValueError("Role must be 'user' or 'admin'")

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        try:
            self.users_collection.insert_one(
                {
                    "username": username,
                    "password": hashed_password,
                    "role": role,
                    "is_first_login": first_login,
                }
            )
            logging.info("Created user %s with role %s", username, role)
        except errors.DuplicateKeyError as exc:
            raise ValueError(f"User {username} already exists") from exc

    # Creating and inserting the animal into the database
    def create_animal(self, animal_data):

        try:
            self.collection.insert_one(animal_data)
            logging.info("Inserted animal %s", animal_data["name"])
        except errors.PyMongoError as e:
            logging.error("Error inserting animal: %s", e)
            return False
        return True

    # Reading all animals
    def read_all_animals(self, query=None):
        try:
            query = query or {}
            cursor = self.collection.find(query)
            logging.info("Read all animals %s", cursor)
            return list(cursor)
        except errors.PyMongoError as e:
            logging.error("Error reading animals: %s", e)
            return []

    # Update animals
    def update_animal(self, animal_id, updated_fields):

        try:
            result = self.collection.update_one({"_id": ObjectId(animal_id)}, {"$set": updated_fields})
            if result.modified_count == 0:
                logging.error("No updates found for animal: %s", animal_id)
                return False
            logging.info("Updated animal: %s", animal_id)
            return True
        except errors.PyMongoError as e:
            logging.error("Error updating animal: %s", e)
            return False

    # Delete animal
    def delete_animal(self, animal_id):

        try:
            result = self.collection.delete_one({"_id": ObjectId(animal_id)})
            if result.deleted_count == 0:
                logging.error("No deletes found for animal: %s", animal_id)
                return False
            logging.info("Deleted animal: %s", animal_id)
            return True
        except errors.PyMongoError as e:
            logging.error("Error deleting animal: %s", e)
            return False
