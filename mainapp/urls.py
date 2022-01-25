from django.urls import path

import mainapp.views as mainapp

app_name = "mainapp"

urlpatterns = [
    path("", mainapp.products, name="index"),
    # path("<int:category_pk>/page/1", mainapp.products, name="category"),
    path("<int:category_pk>/page/<int:page>/", mainapp.products, name="page"),
    path("<int:category_pk>/<int:product_pk>/", mainapp.products, name="product"),
    path("<int:category_pk>/<int:product_pk>/page/<int:page>", mainapp.products, name="page"),
]
