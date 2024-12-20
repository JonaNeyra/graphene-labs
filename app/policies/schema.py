import graphene
from graphene_django import DjangoObjectType

from .models import User, Policy, Dependent, Agent


class AgentType(DjangoObjectType):
    class Meta:
        model = Agent


class UserType(DjangoObjectType):
    class Meta:
        model = User


class PolicyType(DjangoObjectType):
    class Meta:
        model = Policy


class DependentType(DjangoObjectType):
    class Meta:
        model = Dependent


class Query(graphene.ObjectType):
    policies = graphene.List(PolicyType)

    def resolve_policies(self, info):
        return Policy.objects.select_related(
            'holder',
            'agent',
        ).prefetch_related(
            'dependents',
        )


schema = graphene.Schema(query=Query)
