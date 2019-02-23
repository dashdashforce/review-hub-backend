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
        return self.data[user_id]

    async def create_user(self, user_id, user_data):
        self.data[user_id] = user_data