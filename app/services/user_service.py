from ..repository import UserRepository
from tornado.httpclient import HTTPError


class UserService:

    def __init__(self, user_repository):
        self.user_repository = user_repository

    async def get_user(self, user_id):
        user = await self.user_repository.get_user(user_id)
        if not user:
            raise HTTPError(404, 'User not found')
        return user
