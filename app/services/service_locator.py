
from .auth_service import AuthService
from ..clients import github_client


class ServiceLocator:
    auth_service = AuthService(github_client)
