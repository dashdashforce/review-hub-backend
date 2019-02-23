from app.entity_transformer import UserTransformer
from app.repository import UserRepository

user_transformer = UserTransformer()
user_repository = UserRepository()

class UserDataService:
    async def create_user(self, git_user_data):
        user = user_transformer.create_entity(git_user_data)
        user_repository.create_user(user);
