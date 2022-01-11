from django.urls import path

import basketapp.views as basketapp

from .apps import BasketappConfig

app_name = BasketappConfig.name

urlpatterns = [
    path("", basketapp.basket, name='view'),
    path("add/<int:pk>", basketapp.add_to_basket, name="add"),
    path("remove/<int:pk>", basketapp.remove_from_basket, name="remove"),
]
