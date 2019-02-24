import os

from motor.motor_tornado import MotorClient
from tornado.log import app_log


class UserRepository:
    def __init__(self):
        db_url = os.getenv("MONGODB_URL")
        db_name = os.getenv("MONGODB_DB")
        self.collection = MotorClient(db_url)[db_name].users
        self.data = []

    async def get_user(self, user_id):
        return await self.collection.find_one({'_id': user_id})

    async def create_user(self, user_entity):
        try:
            await self.collection.insert_one(user_entity)
        except Exception as e:
            app_log.warn(
                'Cannot save user {}'.format(user_entity))

    async def update_tocken(self, user_id, token):
        try:
            await self.collection.update_one({'_id': user_id}, {'$set': {'token': token}})
        except Exception as e:
            app_log.warn(
                'Cannot update user tocken {}'.format(user_entity))
        
    