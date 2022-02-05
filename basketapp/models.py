from django.conf import settings
from django.db import models
from django.db.models.deletion import CASCADE

from mainapp.models import Product


class Basket(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="basket")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(verbose_name="количество", default=0)
    add_datetime = models.DateTimeField(verbose_name="дата добавления", auto_now_add=True)

    @property
    def product_cost(self):
        return self.quantity * self.product.price

    @classmethod
    def product_count(cls, user):
        products = cls.objects.filter(user=user)
        cls._count = 0
        for item in products:
            cls._count += item.quantity
        return cls._count

    @classmethod
    def total_cost(cls, user):
        products = cls.objects.filter(user=user)
        cls._total_cost = 0
        for item in products:
            cls._total_cost += item.product_cost
        return cls._total_cost

    @staticmethod
    def get_items(user):
        return Basket.objects.filter(user_id=user.id).order_by("product__category")
