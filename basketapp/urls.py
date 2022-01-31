from django.urls import re_path

import basketapp.views as basketapp

from .apps import BasketappConfig

app_name = BasketappConfig.name

urlpatterns = [
    re_path(r"^$", basketapp.basket, name="view"),
    re_path(r"^add/(?P<category_pk>\d+)/(?P<pk>\d+)/$", basketapp.add_to_basket, name="add"),
    re_path(r"^remove/(?P<pk>\d+)/$", basketapp.remove_from_basket, name="remove"),
    re_path(r"^edit/(?P<pk>\d+)/(?P<quantity>\d+)/$", basketapp.edit_quantity, name="edit"),
]
