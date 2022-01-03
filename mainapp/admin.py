from django.contrib import admin

from .models import Category, Contact, Product

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Contact)
