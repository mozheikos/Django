from tabnanny import verbose

from django.conf import settings
from django.db import models
from django.shortcuts import get_object_or_404

from mainapp.models import Product


class Order(models.Model):
    FORMING = "FM"
    SENT_TO_PROCEED = "STP"
    PROCEEDED = "PRD"
    PAID = "PD"
    READY = "RDY"
    CANCEL = "CNC"

    ORDER_STATUS_CHOICES = (
        (FORMING, "формируется"),
        (SENT_TO_PROCEED, "отправлен в обработку"),
        (PAID, "оплачен"),
        (PROCEEDED, "обрабатывается"),
        (READY, "готов к выдаче"),
        (CANCEL, "отменен"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    created = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True)
    updated = models.DateTimeField(
        verbose_name="Дата обовления", auto_now=True)
    status = models.CharField(verbose_name="Статус заказа",
                              max_length=3, choices=ORDER_STATUS_CHOICES, default=FORMING)
    is_active = models.BooleanField(
        verbose_name="Активен", default=True, db_index=True)

    class Meta:
        ordering = ("-created",)
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self) -> str:
        return "Текущий заказ: {}".format(self.id)

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        items = self.orderitems.select_related()
        return len(items)

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity * x.product.price, items)))

    def delete(self):
        for item in self.orderitems.select_related():
            item.product.count += item.quantity
            item.product.save()

        self.is_active = False
        self.status = self.CANCEL
        self.save()

    # def save(self):
     #   for item in self.orderitems.select_related():
      #      if int(item.quantity) == 0:
       #         item.delete()
        # super().save()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="orderitems", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, verbose_name="продукт", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        verbose_name="количество", default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity

    @staticmethod
    def get_item(pk):
        return get_object_or_404(OrderItem, pk=pk)
