from bson.objectid import ObjectId
from pymongo.database import Database
from typing import List, Optional


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
            "coordinates": post["coordinates"],
        }

        self.database["posts"].insert_one(payload)

    def get_post_by_id(self, id: str) -> dict[str, str]:
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
        cursor = self.database["comments"].find({"post_id": ObjectId(id)})
        cursor_list = list(cursor)
        comments = []
        for item in cursor_list:
            comments.append(item["content"])

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

    def get_posts(
        self,
        limit: int,
        offset: int,
        rooms_count: Optional[int] = None,
        type: Optional[str] = None,
        price_from: Optional[float] = None,
        price_until: Optional[str] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        radius: Optional[float] = None,
    ):
        query = {}

        if rooms_count is not None:
            query["rooms_count"] = {}
            query["rooms_count"]["$gt"] = rooms_count

        if type is not None:
            query["type"] = type

        if price_from is not None or price_until is not None:
            query["price"] = {}
            if price_from is not None:
                query["price"]["$gt"] = price_from
            if price_until is not None:
                query["price"]["$lt"] = price_until

        if latitude is not None and longitude is not None and radius is not None:
            new_radius = radius * 3.2535313808
            query["coordinates"] = {
                "$geoWithin": {"$centerSphere": [[longitude, latitude], new_radius]}
            }

        total_count = self.database["posts"].count_documents(query)

        cursor = (
            self.database["posts"].find(query).limit(limit).skip(offset).sort("address")
        )

        result = []
        for item in cursor:
            result.append(item)

        return {"total": total_count, "objects": result}
