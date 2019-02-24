from .base_tentity_transformer import BaseEntityTransformer

class UserTransformer(BaseEntityTransformer):
    def create_entity(self, gitdata):
        return {
            '_id': gitdata['id'],
            'token': gitdata['access_token'],
            'imageUrl': gitdata['avatarUrl'],
            'login': gitdata['login'],
            'name': gitdata['name'],
        }