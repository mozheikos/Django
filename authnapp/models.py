from functools import cached_property
import hashlib
import random
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import PositiveSmallIntegerField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now


class ShopUser(AbstractUser):

    avatar = models.ImageField(upload_to="users_avatars", blank=True)
    age = PositiveSmallIntegerField(verbose_name="возраст", default=20)
    auth_key = models.CharField(max_length=256, blank=True)
    auth_key_is_expired = models.DateTimeField(default=now(), blank=True)

    def is_activation_key_expired(self):
        if now() <= self.auth_key_is_expired:
            return False
        return True

    def get_auth_key(self):
        salt = hashlib.sha1(
            str(random.random()).encode("utf8")).hexdigest()[:6]
        self.auth_key = hashlib.sha1(
            (self.email + salt).encode("utf8")).hexdigest()
        self.auth_key_is_expired = now() + timedelta(hours=48)

    @cached_property
    def basket_items(self):
        return self.basket.select_related()


class ShopUserProfile(models.Model):
    MALE = "M"
    FEMALE = "F"

    GENDER_CHOICES = (
        (MALE, "Муж"),
        (FEMALE, "Жен"),
    )

    user = models.OneToOneField(
        ShopUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name="теги", max_length=128, blank=True)
    aboutMe = models.TextField(
        verbose_name="о себе", max_length=512, blank=True)
    interests = models.TextField(
        verbose_name="интересы", max_length=256, blank=True)
    gender = models.CharField(
        verbose_name="пол", max_length=1, choices=GENDER_CHOICES, blank=True)

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()
