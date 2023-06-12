from bson.objectid import ObjectId
from pymongo.database import Database


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

    def delete_post(self, id: str):
        self.database["posts"].find_one_and_delete({"_id": ObjectId(id)})

    # def get_user_by_id(self, user_id: str) -> dict | None:
    #     user = self.database["users"].find_one(
    #         {
    #             "_id": ObjectId(user_id),
    #         }
    #     )
    #     return user

    # def get_user_by_email(self, email: str) -> dict | None:
    #     user = self.database["users"].find_one(
    #         {
    #             "email": email,
    #         }
    #     )
    #     return user

    # def update_user(self, user_id: str, name: str, phone: str, city: str):
    #     self.database["users"].update_one(
    #         {"_id": ObjectId(user_id)},
    #         {
    #             "$set": {
    #                 "name": name,
    #                 "phone": phone,
    #                 "city": city,
    #             }
    #         },
    #     )
