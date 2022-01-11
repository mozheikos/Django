from django.conf import settings
from django.db import models
from django.db.models.deletion import CASCADE

from mainapp.models import Product


class Basket(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="basket")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        verbose_name="количество", default=0)
    add_datetime = models.DateTimeField(
        verbose_name="дата добавления", auto_now_add=True)
