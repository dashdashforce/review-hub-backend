import re
from collections import OrderedDict
from datetime import datetime

import graphene
from tornado import gen
from tornado.log import app_log
from .services import service_locator

pull_request_service = service_locator.pull_request_service
user_service = service_locator.user_service


class Language(graphene.ObjectType):
    id = graphene.String()
    color = graphene.String()
    name = graphene.String()

    @classmethod
    def map(cls, lang_dict):
        return Language(
            lang_dict['id'],
            lang_dict['color'],
            lang_dict['name']
        )


class Comment(graphene.ObjectType):
    text = graphene.String()
    reviewer_id = graphene.String()
    status = graphene.String()

    @classmethod
    def map(cls, comment_dict):
        return Comment(
            comment_dict['text'],
            comment_dict['reviewer_id'],
            comment_dict['status']
        )


class PullRequest(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    body = graphene.String()
    user_id = graphene.String()
    status = graphene.String()
    repo_name = graphene.String()
    langs = graphene.List(Language)
    comments = graphene.List(Comment)

    @classmethod
    def map(cls, pr_dict):
        return PullRequest(
            pr_dict['_id'],
            pr_dict['name'],
            pr_dict['body'],
            pr_dict['user_id'],
            pr_dict['status'],
            pr_dict['repo_name']
        )

    def resolve_langs(self):
        return map(Language.map, [])

    def resolve_comments(self):
        return map(Comment.map, [])


class User(graphene.ObjectType):
    id = graphene.String()
    image_url = graphene.String()
    login = graphene.String()
    name = graphene.String()
    langs = graphene.List(Language)
    pull_requests = graphene.List(PullRequest)

    review_requests_count = graphene.Int()
    code_reviews_count = graphene.Int()

    @classmethod
    def map(cls, user_dict):
        return User(
            user_dict['_id'],
            user_dict['imageUrl'],
            user_dict['login'],
            user_dict['name'],
            map(Language.map, user_dict['langs'])
        )

    def resolve_pull_requests(self, info):
        return map(PullRequest.map, [])

    def resolve_review_requests_count(self, info):
        return 0

    def resolve_code_reviews_count(self, info):
        return 0


class Query(graphene.ObjectType):
    user = graphene.Field(User, id=graphene.String())

    pull_request = graphene.Field(PullRequest, id=graphene.String())

    pull_requests_feed = graphene.List(PullRequest)

    review_requests = graphene.List(PullRequest)

    async def resolve_pull_requests_feed(self, info):
        pull_requests_result = await pull_request_service.get_pull_requests_feed()
        return map(PullRequest.map, pull_requests_result)

    async def resolve_review_requests(self, info):
        pull_requests_result = await pull_request_service.get_pull_requests_by_user_id(info.context.authentication['id'])
        return map(PullRequest.map, pull_requests_result)

    async def resolve_user(self, info):
        id = info.context.authentication['id']
        return User.map(await user_service.get_user(id))

    def resolve_pull_request(self, info):
        return PullRequest.map({})

class SharePullRequest(graphene.Mutation):
    class Arguments:
        pull_request_id = graphene.String()

    ok = graphene.Boolean()

    async def mutate(self, info, pull_request_id):
        ok = True
        await pull_request_service.share_request_to_review(pull_request_id)
        return SharePullRequest(ok=ok)

class SubmitRequestToReview(graphene.Mutation):
    class Arguments:
        pull_request_id = graphene.String()

    ok = graphene.Boolean()

    async def mutate(self, info, pull_request_id):
        ok = True
        await pull_request_service.submit_request_to_review(pull_request_id)
        return SubmitRequestToReview(ok=ok)

class MyMutations(graphene.ObjectType):
    share_pull_request = SharePullRequest.Field()
    submit_request_to_review = SubmitRequestToReview.Field()


schema = graphene.Schema(query=Query, mutation=MyMutations)
