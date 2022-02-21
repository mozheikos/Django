from django.core.management.base import BaseCommand
from django.db import connection
from django.db.models import Q, When, Case, F
from mainapp.models import db_profile_by_type, Product
from ordersapp.models import OrderItem
from datetime import timedelta


class Command(BaseCommand):
    def handle(self, *args, **options):
        query_1 = Product.objects.filter(
            (Q(category__title="дом") | Q(
                category__title="офис")) & Q(price__gte=1000) & Q(price__lte=3000)
        )
        for q in query_1:
            print(f'{q}: {q.price}')
        print("-" * 20)
        query_2 = Product.objects.filter(
            (
                (Q(category__title="офис") | Q(category__title="классика") | Q(category__title="прогресс")) & Q(
                    count__gte=20)
            ) | (
                Q(category__title="дом") & Q(count__lt=10)
            )
        ).annotate(cost=F('price') * F('count'))
        for q in query_2:
            print(
                f'{q}: количество - {q.count} шт, цена - {q.price} руб/шт, стоимость - {round(q.cost, 2)} руб.')
