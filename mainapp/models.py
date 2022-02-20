from functools import cached_property
from django.db import models
from django.db.models.deletion import CASCADE


class Category(models.Model):
    title = models.CharField(
        verbose_name="Название категории", max_length=64, unique=True)
    description = models.TextField(
        verbose_name="описание категории", blank=True)
    is_active = models.BooleanField(
        verbose_name="категория активна", default=True, db_index=True)

    def __str__(self) -> str:
        return self.title

    def save(self):
        products = self.product_set.select_related()
        for product in products:
            product.is_active = self.is_active
            product.save()
        super(Category, self).save()

    @cached_property
    def category_products(self):
        return self.product_set.select_related().exclude(is_active=False)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=CASCADE)
    name = models.CharField(verbose_name="название продукта", max_length=128)
    image = models.ImageField(upload_to="products_images", blank=True)
    short_desc = models.CharField(
        verbose_name="краткое описание", max_length=60, blank=True)
    description = models.TextField(verbose_name="описание", blank=True)
    price = models.DecimalField(
        verbose_name="цена", max_digits=8, decimal_places=2, default=0)
    count = models.PositiveIntegerField(
        verbose_name="количество на складе", default=0)
    is_active = models.BooleanField(
        verbose_name="продукт активен", default=True, db_index=True)

    def __str__(self) -> str:
        return f"{self.name} - ({self.category.title})"

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True)


class Contact(models.Model):
    city = models.CharField(verbose_name="город", max_length=120)
    phone = models.CharField(verbose_name="телефон", max_length=20)
    mail = models.EmailField(verbose_name="e-mail", max_length=64)
    address = models.CharField(verbose_name="адрес", max_length=255)
