from django.db import models
from django.db.models.deletion import CASCADE


class Category(models.Model):
    title = models.CharField(
        verbose_name='Название категории', max_length=64, unique=True)
    description = models.TextField(
        verbose_name='описание категории', blank=True)

    def __str__(self) -> str:
        return self.title


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=CASCADE)
    name = models.CharField(verbose_name='название продукта', max_length=128)
    image = models.ImageField(upload_to='products_images', blank=True)
    short_desc = models.CharField(
        verbose_name='краткое описание', max_length=60, blank=True)
    description = models.TextField(verbose_name='описание', blank=True)
    price = models.DecimalField(
        verbose_name='цена', max_digits=8, decimal_places=2, default=0)
    count = models.PositiveIntegerField(
        verbose_name='количество на складе', default=0)

    def __str__(self) -> str:
        return f'{self.name} - ({self.category.title})'
