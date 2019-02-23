import re
from collections import OrderedDict
from datetime import datetime

import graphene
from tornado import gen
from tornado.log import app_log

class PullRequest(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    userId = graphene.String()
    status = graphene.String()
    langs = graphene.String()
    reviewers = graphene.List()
    comments = graphene.List()

class Language(graphene.ObjectType):
    id = graphene.String()
    color = graphene.String()
    name = graphene.String()

class User(graphene.ObjectType):
    id = graphene.String()
    token = graphene.String()
    image_url = graphene.String()
    langs = graphene.List(Language)
    pull_requests = 

class Query(graphene.ObjectType):
    user = graphene.Field(User, id=graphene.String())

    def resolve_test(self, info):
        return 'Hello world {}'.format(info.context.authentication)



schema = graphene.Schema(query=Query)
