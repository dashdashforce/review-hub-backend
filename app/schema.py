import re
from collections import OrderedDict
from datetime import datetime

import graphene
from tornado import gen
from tornado.log import app_log

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
    code = graphene.String()
    user_id = graphene.String()
    status = graphene.String()
    langs = graphene.List(Language)
    comments = graphene.List(Comment)

    @classmethod
    def map(cls, pr_dict):
        return PullRequest(
            pr_dict['id'],
            pr_dict['name'],
            pr_dict['code'],
            pr_dict['user_id'],
            pr_dict['status'],
            pr_dict['langs'],
            pr_dict['comments']
        )

    async def resolve_langs(self):
        return map(Language.map, [])
    
    async def resolve_comments(self):
        return map(Comment.map, [])

class User(graphene.ObjectType):
    id = graphene.String()
    token = graphene.String()
    image_url = graphene.String()
    langs = graphene.List(Language)
    pull_requests = graphene.List(PullRequest)

    async def resolve_langs(self):
        return map(Language.map, [])

class Query(graphene.ObjectType):
    user = graphene.Field(User, id=graphene.String())

    pull_request = graphene.Field(PullRequest, id=graphene.String())

    async def resolve_pull_request(self, info):
        return PullRequest.map({})



schema = graphene.Schema(query=Query)
