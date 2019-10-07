# -*- coding: utf-8 -*-
import graphene

from testform.queries.bases import OrgsQuery
from testform.queries.kartoteka import KartotekaQuery


class Query(OrgsQuery, KartotekaQuery, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)