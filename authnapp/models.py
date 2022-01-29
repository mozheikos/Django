import hashlib
import random
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import PositiveSmallIntegerField
from django.utils.timezone import now


class ShopUser(AbstractUser):

    avatar = models.ImageField(upload_to="users_avatars", blank=True)
    age = PositiveSmallIntegerField(verbose_name="возраст", default=20)
    auth_key = models.CharField(max_length=256, blank=True)
    auth_key_is_expired = models.DateTimeField(default=(now() + timedelta(hours=48)))

    def is_activation_key_expired(self):
        if now() <= self.auth_key_is_expired:
            return False
        return True

    def get_auth_key(self):
        salt = hashlib.sha1(str(random.random()).encode("utf8")).hexdigest()[:6]
        self.auth_key = hashlib.sha1((self.email + salt).encode("utf8")).hexdigest()
        self.auth_key_is_expired = now() + timedelta(hours=48)
