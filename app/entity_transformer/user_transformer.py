from .base_tentity_transformer import BaseEntityTransformer

class UserTransformer(BaseEntityTransformer):
    def create_entity(self, gitdata):
        return {
            '_id': ['id'],
            'token': 'temp',
            'imageUrl': gitdata['avatarUrl'],
            'login': gitdata['login']
        }