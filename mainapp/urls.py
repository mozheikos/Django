from django.urls import path, re_path

import mainapp.views as mainapp

app_name = "mainapp"

urlpatterns = [
    re_path(r"^$", mainapp.products, name="index"),
    re_path(r"^(?P<category_pk>\d+)/page/(?P<page>\d+)/$", mainapp.products, name="page"),
    re_path(r"^(?P<category_pk>\d+)/(?P<product_pk>\d+)/$", mainapp.products, name="product"),
    re_path(r"^(?P<category_pk>\d+)/(?P<product_pk>\d+)/page/(?P<page>\d+)/$", mainapp.products, name="page"),
]
