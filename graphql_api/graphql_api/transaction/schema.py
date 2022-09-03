import graphene
from graphql_api.transaction.models import Transaction
from graphene import Node
from graphene_django.types import DjangoObjectType
from datetime import timedelta
from django.utils import timezone
from graphene_django.filter import DjangoFilterConnectionField
from dateutil.relativedelta import relativedelta 
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.db.models.functions import ExtractWeek
from datetime import date

class TransactionNode(DjangoObjectType):
    class Meta:
        model = Transaction
        interfaces = (Node,)
        fields = "__all__"
        filter_fields = ['']

    pk = graphene.String()

class CategoryType(DjangoObjectType):
    class Meta:
        model = Transaction
        fields = "__all__"


class TransactionQueries(graphene.ObjectType):
    transactions = graphene.List(TransactionNode)
    category = graphene.Field(lambda: graphene.List(CategoryType), presetRange=graphene.String(required=True))
    date = graphene.List(CategoryType, presetRange=graphene.String(required=True))

    def resolve_transactions(self, info):
        return Transaction.objects.all().order_by("-created_at")

    # EXTEND THIS CODE
    
    def resolve_category(self, info, presetRange=None, **kwargs):
        if presetRange=="Last 7 days":
            return Transaction.objects\
                .filter(created_at__gte=timezone.now().date() - timedelta(days=7))\
                    .values('category', 'created_at')\
                        .annotate(amount=Sum('amount'))
        elif presetRange=="Last 7 weeks":
            return Transaction.objects\
                .filter(created_at__gte=timezone.now().date() - relativedelta(weeks=+7))\
                    .values('category')\
                        .annotate(amount=Sum('amount'))
        elif presetRange=="Last 7 months":
            return Transaction.objects\
                .filter(created_at__gte=timezone.now().date() - relativedelta(months=+7))\
                    .values('category')\
                        .order_by('-created_at')\
                            .annotate(amount=Sum('amount'))

    def resolve_date(self, info, presetRange=None, **kwargs): 
        if presetRange=="Last 7 days":
            return Transaction.objects\
                .filter(created_at__gte=date.today() - timedelta(days=7))\
                    .values('created_at')\
                        .annotate(amount=Sum('amount'))
        elif presetRange=="Last 7 weeks":
            return Transaction.objects\
                .filter(created_at__gte=timezone.now().date() - relativedelta(weeks=+7))\
                    .annotate(week=ExtractWeek('created_at'))\
                        .values('week')\
                            .annotate(amount=Sum('amount'))
        elif presetRange=="Last 7 months":
            return Transaction.objects\
                .filter(created_at__gte=timezone.now().date() - relativedelta(weeks=+7))\
                    .annotate(month=TruncMonth('created_at'))\
                        .values('month')\
                            .annotate(amount=Sum('amount'))



