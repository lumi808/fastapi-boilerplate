from bson.objectid import ObjectId
from pymongo.database import Database
from typing import List


class ShanyraksRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_post(self, post: dict):
        payload = {
            "post_id": ObjectId(post["post_id"]),
            "type": post["type"],
            "price": post["price"],
            "address": post["address"],
            "area": post["area"],
            "rooms_count": post["rooms_count"],
            "description": post["description"],
            "media": [],
        }

        self.database["posts"].insert_one(payload)

    def get_post_by_id(self, id: str) -> dict:
        post = self.database["posts"].find_one({"_id": ObjectId(id)})

        return post

    def update_post(
        self,
        id: str,
        type: str,
        price: float,
        address: str,
        area: float,
        rooms_count: int,
        description: str,
    ):
        self.database["posts"].update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "type": type,
                    "price": price,
                    "address": address,
                    "area": area,
                    "rooms_count": rooms_count,
                    "description": description,
                }
            },
        )

    def update_post_media(self, id: str, media: List[str]):
        self.database["posts"].update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "media": media,
                },
            },
        )

    def delete_post(self, id: str):
        self.database["posts"].find_one_and_delete({"_id": ObjectId(id)})

    def add_comment(self, post: dict[str, str]):
        payload = {
            "post_id": ObjectId(post["post_id"]),
            "content": post["content"],
        }
        self.database["comments"].insert_one(payload)

    def get_comments(self, id: str):
        cursor = self.database["comments"].find({"post_id": id})
        comments = []

        for comment in cursor:
            comment_dict = {
                "_id": str(comment["_id"]),
                "post_id": str(comment["post_id"]),
                "content": comment["content"],
                # Include other fields as needed
            }
            comments.append(comment_dict)
        return comments

    def delete_comment(self, comment_id: str):
        self.database["comments"].find_one_and_delete({"_id": ObjectId(comment_id)})

    def update_comment(self, comment_id: str, content: str):
        self.database["comments"].update_one(
            {"_id": ObjectId(comment_id)},
            {
                "$set": {
                    "content": content,
                },
            },
        )
