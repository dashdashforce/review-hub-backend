import os

from motor.motor_tornado import MotorClient
from tornado.log import app_log

class RequestRepository:
    def __init__(self):
        db_url = os.getenv("MONGODB_URL")
        db_name = os.getenv("MONGODB_DB")
        self.collection = MotorClient(db_url)[db_name].request

    async def get_requests_by_user(self, user_id):
        return {{'name': 'new','userId': user_id,'status': 0}, {'name': 'inreview','userId': user_id,'status': 2},{'name': 'closed','userId': user_id,'status': 1}}

    async def get_reviewer_liked_commented_requests(self, user_id):
        return {{'name': 'closed','userId': user_id,'status': 1}}

    async def get_all_reviewer_commented_requests(self, user_id):
        return {{'name': 'new','userId': user_id,'status': 0}, {'name': 'inreview','userId': user_id,'status': 2},{'name': 'closed','userId': user_id,'status': 1}}