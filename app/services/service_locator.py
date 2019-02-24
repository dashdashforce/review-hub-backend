
from .auth_service import AuthService
from .user_service import UserService
from ..clients import github_client
from ..repository import user_repository
from ..entity_transformer import UserTransformer
from ..entity_transformer import RequestTransformer


class ServiceLocator:
    auth_service = AuthService(
        github_client, user_repository, UserTransformer())
    user_service = UserService(user_repository)
