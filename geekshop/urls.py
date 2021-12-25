from django.contrib import admin
from django.urls import path

import mainapp.views as mainapp

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mainapp.main, name='main'),
    path("products/", mainapp.products, name='products'),
    path("products/all", mainapp.products, name="all"),
    path("products/home", mainapp.products, name="home"),
    path("products/office", mainapp.products, name="office"),
    path("products/modern", mainapp.products, name="modern"),
    path("products/classic", mainapp.products, name="classic"),
    path("contact/", mainapp.contact, name='contact'),
]
