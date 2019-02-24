from .base_tentity_transformer import BaseEntityTransformer


class RequestTransformer(BaseEntityTransformer):
    def create_entity(self, gitdata):
        return {
            '_id': gitdata['id'],
            'user_id': gitdata['user_id'],
            'name': gitdata['title'],
            'body': gitdata['body'],
            'repo_name': gitdata['repo_name'],
            'status': 0,
            'langs': gitdata['langs'],
            'commits': gitdata['commits']['nodes'],
            'reviewers': [],
            'comments': [],
        }
