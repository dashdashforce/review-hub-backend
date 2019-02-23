from .base_tentity_transformer import BaseEntityTransformer

class RequestTransformer(BaseEntityTransformer):
    def transform_git_data(self, gitdata, entity):
        []

    def create_entity(self, gitdata):
        return {
            '_id': None,
            'userId': 'temp',
            'name': 'temp',
            'token': 'temp',
            'status': 0,
            'langs': [],
            'reviewers': [],
            'comments': [],
        }