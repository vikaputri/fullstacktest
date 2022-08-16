import graphene
from graphql_api.transaction.models import Transaction
from graphene import Node
from graphene_django.types import DjangoObjectType


class TransactionNode(DjangoObjectType):
    class Meta:
        model = Transaction
        interfaces = (Node,)
        fields = "__all__"
        filter_fields = []

    pk = graphene.String()


class TransactionQueries(graphene.ObjectType):
    transactions = graphene.List(TransactionNode)

    def resolve_transactions(self, info):
        return Transaction.objects.all().order_by("-created_at")

    # EXTEND THIS CODE
