import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from .models import People


class PeopleModel(DjangoObjectType):
    class Meta:
        model = People


class PeopleInput(graphene.InputObjectType):
    guid = graphene.ID()
    role = graphene.String()
    login = graphene.String()
    password = graphene.String()
