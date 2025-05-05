import logging
import os
from typing import Optional, Dict, Tuple, List, Union, Any
import bcrypt
from bson.objectid import ObjectId
from pymongo import MongoClient, errors


class AnimalDatabase:
    """
    Handles MongoDB interactions including user management and CRUD operations for rescue animals.
    """

    def __init__(
        self,
        mongo_uri: Optional[str] = None,
        database: str = "rescue_animals_db",
        collection: str = "animals",
        user_collection: str = "users"
    ) -> None:
        self._mongo_uri = mongo_uri or os.getenv("MONGO_URI", "mongodb://localhost:27017")
        self._database = database
        self._collection_name = collection
        self._user_collection_name = user_collection
        self._connect()

    def _connect(self) -> None:
        try:
            self.client = MongoClient(self._mongo_uri, serverSelectionTimeoutMS=3000)
            self.client.admin.command("ping")
            db = self.client[self._database]
            self.collection = db[self._collection_name]
            self.users = db[self._user_collection_name]
            self.users.create_index("username", unique=True)

            logging.info("Connected to MongoDB: %s", self._mongo_uri)

            if self.users.count_documents({}) == 0:
                default_pwd = os.getenv("ADMIN_PASSWORD", "admin1234")
                logging.info("Creating default admin user")
                self.create_user("admin", default_pwd, role="admin", first_login=True)

        except errors.ConnectionFailure as exc:
            logging.error("Failed to connect to MongoDB: %s", exc)
            raise RuntimeError("Unable to connect to MongoDB") from exc

    @staticmethod
    def is_admin(user: Dict[str, Any]) -> bool:
        return user.get("role") == "admin"

    def authenticate_user(self, username: str, password: str) -> Tuple[Optional[Dict], bool]:
        user = self.users.find_one({"username": username})
        if user and bcrypt.checkpw(password.encode(), user["password"]):
            return user, bool(user.get("is_first_login"))
        return None, False

    def create_user(self, username: str, password: str, role: str = "user", *, first_login: bool = True) -> None:
        if role not in {"user", "admin"}:
            raise ValueError("Role must be 'user' or 'admin'")

        if self.users.find_one({"username": username}):
            raise ValueError(f"Username {username} already exists")

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        try:
            self.users.insert_one({
                "username": username,
                "password": hashed,
                "role": role,
                "is_first_login": first_login
            })
            logging.info("User %s created with role %s", username, role)
        except errors.DuplicateKeyError as exc:
            raise ValueError(f"User {username} already exists") from exc

    def create_animal(self, animal_data: Dict[str, Any]) -> bool:
        try:
            self.collection.insert_one(animal_data)
            logging.info("Animal inserted: %s", animal_data.get("name"))
            return True
        except errors.PyMongoError as exc:
            logging.error("Failed to insert animal: %s", exc)
            return False

    def read_all_animals(self, query: Optional[Dict] = None) -> List[Dict]:
        try:
            return list(self.collection.find(query or {}))
        except errors.PyMongoError as exc:
            logging.error("Failed to read animals: %s", exc)
            return []

    def update_animal(self, animal_id: Union[str, ObjectId], updated_fields: Dict[str, Any]) -> bool:
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(animal_id)},
                {"$set": updated_fields}
            )
            return result.modified_count > 0
        except errors.PyMongoError as exc:
            logging.error("Failed to update animal: %s", exc)
            return False

    def delete_animal(self, animal_id: Union[str, ObjectId]) -> bool:
        try:
            result = self.collection.delete_one({"_id": ObjectId(animal_id)})
            return result.deleted_count > 0
        except errors.PyMongoError as exc:
            logging.error("Failed to delete animal: %s", exc)
            return False
