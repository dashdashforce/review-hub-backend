from .base_tentity_transformer import BaseEntityTransformer

class UserTransformer(BaseEntityTransformer):
    def transform_git_data(self, gitdata, entity):
        entity['node'] = 'temp'
        entity['token'] = 'temp'
        entity['imageUrl'] = 'temp'
        entity['langs'] = []

    def create_entity(self, gitdata):
        return {
            '_id': None,
            'node': 'temp',
            'token': 'temp',
            'imageUrl': 'temp',
            'langs': []
        }