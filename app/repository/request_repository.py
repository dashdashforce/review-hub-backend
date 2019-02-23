import os

from motor.motor_tornado import MotorClient
from tornado.log import app_log


class RequestRepository:
    def __init__(self):
        db_url = os.getenv("MONGODB_URL")
        db_name = os.getenv("MONGODB_DB")
        self.collection = MotorClient(db_url)[db_name].request

    async def get_request(self, request_id):
        return await self.collection.find_one({'_id': request_id})

    async def create_request(self, request): 
        try:
            await self.collection.insert_one(request)
        except Exception as e:
            app_log.warn(
                'Cannot save pull request {}'.format(request))

    async def update_request(self, request):
        try:
            await self.collection.update_one({'_id': request['_id']}, {"$set": request}, upsert=False)
        except Exception as e:
            app_log.warn(
                'Cannot update pull request {}'.format(request))            