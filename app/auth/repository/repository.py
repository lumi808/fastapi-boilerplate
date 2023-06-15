from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId
from pymongo.database import Database

from ..utils.security import hash_password


class AuthRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_user(self, user: dict):
        payload = {
            "email": user["email"],
            "password": hash_password(user["password"]),
            "name": user["name"],
            "city": user["city"],
            "phone": user["phone"],
            "created_at": datetime.utcnow(),
            "favourites": [],
        }

        self.database["users"].insert_one(payload)

    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        return user

    def get_user_by_email(self, email: str) -> Optional[dict]:
        user = self.database["users"].find_one(
            {
                "email": email,
            }
        )
        return user

    def update_user(self, user_id: str, name: str, phone: str, city: str):
        self.database["users"].update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "name": name,
                    "phone": phone,
                    "city": city,
                }
            },
        )

    def get_favourites(self, user_id: str):
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )

        favourites = user["favourites"]
        return favourites

    def add_favourties(self, user_id: str, post_id: str):
        favorites = self.get_favourites(user_id)
        favorites.append(post_id)

        self.database["users"].update_one(
            {"_id": ObjectId(user_id)}, {"$set": {"favourites": favorites}}
        )

    def get_user_favourites_by_id(self, user_id: str):
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        # add addres for every post
        favourites = user["favourites"]
        return favourites

    def delete_favourite(self, user_id: str, post_id: str):
        favorites = self.get_favourites(user_id)
        index = favorites.index(post_id)
        favorites.pop(index)
        self.database["users"].update_one(
            {"_id": ObjectId(user_id)}, {"$set": {"favourites": favorites}}
        )
