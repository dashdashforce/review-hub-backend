
from .auth_service import AuthService
from ..clients import github_client
from ..repository import UserRepository
from ..repository import RequestRepository
from ..entity_transformer import UserTransformer
from ..entity_transformer import RequestTransformer

class ServiceLocator:
    auth_service = AuthService(github_client, UserRepository(), UserTransformer(), RequestRepository(), RequestTransformer())
