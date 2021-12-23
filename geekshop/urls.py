from django.contrib import admin
from django.urls import path

import mainapp.views as mainapp

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mainapp.main),
    path("index.html", mainapp.main),
    path("products.html", mainapp.products),
    path("contact.html", mainapp.contact),
]
