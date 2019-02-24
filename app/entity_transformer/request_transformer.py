from .base_tentity_transformer import BaseEntityTransformer


class RequestTransformer(BaseEntityTransformer):
    def create_entity(self, gitdata):
        return {
            '_id': gitdata['id'],
            'user_id': gitdata['user_id'],
            'name': 'temp',
            'repo_name': gitdata['repo_name'],
            'token': 'temp',
            'status': 0,
            'langs': [],
            'commits': gitdata['commits']['nodes'],
            'reviewers': [],
            'comments': [],
        }
