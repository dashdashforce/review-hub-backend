import re
from collections import OrderedDict
from datetime import datetime

import graphene
from tornado import gen
from tornado.log import app_log


class Query(graphene.ObjectType):
    test = graphene.String()

    def resolve_test(self, info):
        return 'Hello world'


schema = graphene.Schema(query=Query)
