import datetime
import json

from django.conf import settings
from django.shortcuts import render

from .models import Category, Product


def get_controller_data(file_name):
    with open(f"data_json/{file_name}", "r") as f:
        data = json.load(f)
    return data


def main(request):
    title = "Главная"

    products = Product.objects.all()

    content = {"title": title, "products": products,
               "media_url": settings.MEDIA_URL}
    return render(request, "mainapp/index.html", content)


def products(request, category_pk=1, product_pk=None):
    title = "продукты"
    links = Category.objects.all()
    product_large = None
    if category_pk == 1:
        same_products = Product.objects.all()
    else:
        same_products = Product.objects.filter(category_id=category_pk)
    if product_pk:
        product_large = Product.objects.get(pk=product_pk)
        category_pk = Category.objects.get(id=product_large.category.id)
        same_products = Product.objects.filter(category_id=category_pk)

    content = {
        "title": title,
        "links": links,
        "same_products": same_products,
        "product_large": product_large,
        "media_url": settings.MEDIA_URL,
    }
    if category_pk:
        print(f"User select category: {category_pk}")
    return render(request, "mainapp/products.html", content)


def contact(request):
    title = "о нас"

    contact_cards = get_controller_data("cities.json")
    today = datetime.datetime.now()

    content = {"title": title, "visit_date": today,
               "contact_cards": contact_cards}
    return render(request, "mainapp/contact.html", content)
