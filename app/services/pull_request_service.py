from app.entity_transformer import RequestTransformer
from app.repository import RequestRepository

request_repository = RequestRepository()
request_transformer = RequestTransformer()

class PullRequestService:
    NEW_STATUS = 0
    APPROVING_STATUS = 2
    PROCCESING_STATUS = 1
    PENDING_STATUS = 3

    async def assign_pull_request(self, user_id, pr_id):
        pr = await request_repository.get_request(pr_id)
        
        if  user_id not in pr['reviewers']:
            pr['reviewers'].append(user_id)
            request_repository.update_request(pr)

        if pr['status'] == PullRequestService.PENDING_STATUS:
            pr['status'] = PullRequestService.PROCCESING_STATUS

    async def add_comment_to_pr(self, pr_id, reviewer_id, text):
        pr = await request_repository.get_request(pr_id)
        # add user comment check
        pr['comments'].append({
            'text': text,
            'reviewerId': reviewer_id,
            'status': 0
        })

        request_repository.update_request(pr)

    async def change_comment_status(self, pr_id, reviewer_id, status):
        pr = await request_repository.get_request(pr_id)
        comments = []

        if status == PullRequestService.APPROVING_STATUS and pr['status'] != PullRequestService.APPROVING_STATUS:
            pr['status'] = PullRequestService.APPROVING_STATUS

        for comment in pr['comments']:
            if comment['reviewerId'] == reviewer_id:
                comment['status'] = status
            comments.append(comment)

        pr['comments'] = comments
        request_repository.update_request(pr)

    async def get_pull_requests_feed(self):
        requests = await request_repository.get_all_pull_requests_per_status(PullRequestService.PENDING_STATUS)
        return requests

    async def submit_request_to_review(self):
        pass
    
    def create_pull_request(self, github_pr_data):
        pull_request = request_transformer.create_entity(github_pr_data)
        request_repository.create_request(pull_request)