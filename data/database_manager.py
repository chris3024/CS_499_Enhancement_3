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
                 database: str = "rescue_animals_db", collection: str = "animals", user_collection: str = "users") -> None:
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

            self.users_collection.create_index("username", unique=True)

            # Debug statement
            logging.info("MONGO URI → %s", mongo_uri)
            logging.info("Connected to MongoDB %s", database)

            # Adding default admin on first run
            if self.users_collection.count_documents({}) == 0:
                print("No users found....Creating default user")
                default_pwd = os.getenv("ADMIN_PASSWORD", "admin1234")
                self.create_user("admin", default_pwd, "admin", first_login=True)

        except errors.ConnectionFailure as exc:
            logging.error("Error connecting to MongoDB: %s", exc)
            raise RuntimeError("Error connecting to MongoDB") from exc

    # Used to check user role
    @staticmethod
    def is_admin(user: dict) -> bool:
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

        if self.users_collection.find_one({"username": username}):
            raise ValueError(f"Username {username} already exists")

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
    def create_animal(self, animal_data: dict) -> bool:

        try:
            self.collection.insert_one(animal_data)
            logging.info("Inserted animal %s", animal_data["name"])
            return True
        except errors.PyMongoError as e:
            logging.error("Error inserting animal: %s", e)
            return False


    # Reading all animals
    def read_all_animals(self, query: dict | None = None) -> list[dict]:
        try:
            cursor = self.collection.find(query or {})
            return list(cursor)
        except errors.PyMongoError as exc:
            logging.error("Error reading animals: %s", exc)
            return []

    # Update animals
    def update_animal(self, animal_id: str | ObjectId, updated_fields: dict) -> bool:

        try:
            result = self.collection.update_one(
                {"_id": ObjectId(animal_id)}, {"$set": updated_fields})
            return result.modified_count > 0
        except errors.PyMongoError as e:
            logging.error("Error updating animal: %s", e)
            return False

    # Delete animal
    def delete_animal(self, animal_id: str | ObjectId) -> bool:

        try:
            result = self.collection.delete_one({"_id": ObjectId(animal_id)})
            return result.deleted_count > 0
        except errors.PyMongoError as e:
            logging.error("Error deleting animal: %s", e)
            return False
