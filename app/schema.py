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
    reviewerId = graphene.String()
    status = graphene.String()

class PullRequest(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    code = graphene.String()
    userId = graphene.String()
    status = graphene.String()
    langs = graphene.List(Language)
    comments = graphene.List(Comment)

class User(graphene.ObjectType):
    id = graphene.String()
    token = graphene.String()
    image_url = graphene.String()
    langs = graphene.List(Language)
    pull_requests = graphene.List(PullRequest)

class Query(graphene.ObjectType):
    user = graphene.Field(User, id=graphene.String())

    pull_request = graphene.Field(PullRequest, id=graphene.String())

    def resolve_test(self, info):
        return 'Hello world {}'.format(info.context.authentication)



schema = graphene.Schema(query=Query)
