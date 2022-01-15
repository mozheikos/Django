from django.urls import path

import basketapp.views as basketapp

from .apps import BasketappConfig

app_name = BasketappConfig.name

urlpatterns = [
    path("", basketapp.basket, name="view"),
    path("add/<int:category_pk>/<int:pk>", basketapp.add_to_basket, name="add"),
    path("remove/<int:pk>", basketapp.remove_from_basket, name="remove"),
    path("edit/<int:pk>/<int:quantity>", basketapp.edit_quantity, name="edit"),
]
