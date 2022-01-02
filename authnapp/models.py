from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import PositiveSmallIntegerField


class ShopUser(AbstractUser):

    avatar = models.ImageField(upload_to="users_avatars", blank=True)
    age = PositiveSmallIntegerField(verbose_name="возраст", default=20)
