
from .auth_service import AuthService
from ..clients import github_client
from ..repository import UserRepository
from ..entity_transformer import UserTransformer

class ServiceLocator:
    auth_service = AuthService(github_client, UserRepository(), UserTransformer())
