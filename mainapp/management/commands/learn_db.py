from django.core.management.base import BaseCommand
from django.db import connection
from django.db.models import Q, When, Case, F
from django.forms import CharField, DateTimeField, DecimalField
from mainapp.models import db_profile_by_type, Product
from ordersapp.models import OrderItem
from datetime import timedelta, datetime, time


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

        """
        Взял за основу задачу с урока, постарался сделать не заглядывая, бизнес-логика мне не очень понятна,
        потому волны не совсем такие получились.
        """

        discount_1 = 30
        discount_2 = 15

        disc_timedelta_1 = timedelta(hours=12)
        disc_timedelta_2 = timedelta(hours=24)

        discount = Case(
            When(Q(order__updated__lte=F('order__created') +
                 disc_timedelta_1), then=discount_1),
            When(Q(order__updated__lte=F('order__created') +
                 disc_timedelta_2), then=discount_2),
            default=5
        )

        expires = Case(
            When(Q(discount=discount_1), then=disc_timedelta_1),
            When(Q(discount=discount_2), then=disc_timedelta_2),
            default=timedelta(days=30),
        )

        query = OrderItem.objects.filter().annotate(discount=discount).annotate(expires=expires).annotate(
            new_price=F('product__price') * (100 - F('discount')) / 100).order_by("-discount", "new_price")
        header = f' № | № заказа | ID пользователя |   Название   |   Цена   | Скидка | Цена со скидкой |       Создан        |    Акция истекает    |'
        print()
        print(header)
        print()
        for item in query:
            string = f"{str(item.id).center(3, ' ')}|{str(item.order.id).center(10, ' ')}|"\
                f"{str(item.order.user.id).center(16, ' ')} |"\
                f"{(item.product.name).center(14, ' ')}|{str(item.product.price).center(10, ' ')}|"\
                f"{str(abs(item.discount)).center(8, ' ')}|{str(abs(round(item.new_price, 2))).center(17, ' ')}| "\
                f"{item.order.created.strftime('%d %b %Y - %H:%M')} | {(item.order.created + item.expires).strftime('%d %b %Y  - %H:%M')} |"
            print(string)
