import json

from django.conf import settings
from django.shortcuts import render
from django.utils import timezone

from basketapp.models import Basket

from .models import Category, Contact, Product


def get_controller_data(file_name):
    with open(f"data_json/{file_name}", "r") as f:
        data = json.load(f)
    return data


def main(request):
    title = "Главная"

    products = Product.objects.all()
    basket_count = Basket.product_count(request.user)
    basket_cost = Basket.total_cost(request.user)

    content = {
        "title": title,
        "products": products,
        "media_url": settings.MEDIA_URL,
        "basket_count": basket_count,
        "basket_cost": basket_cost,
    }
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
        same_products = Product.objects.filter(category_id=category_pk).exclude(pk=product_pk)

    basket_count = Basket.product_count(request.user)
    basket_cost = Basket.total_cost(request.user)
    content = {
        "title": title,
        "links": links,
        "same_products": same_products,
        "product_large": product_large,
        "media_url": settings.MEDIA_URL,
        "category": category_pk,
        "basket_count": basket_count,
        "basket_cost": basket_cost,
    }
    if category_pk:
        print(f"User select category: {category_pk}")
    return render(request, "mainapp/products.html", content)


def contact(request):
    title = "о нас"

    basket_count = Basket.product_count(request.user)
    basket_cost = Basket.total_cost(request.user)
    contact_cards = Contact.objects.all()
    today = timezone.now()

    content = {
        "title": title,
        "visit_date": today,
        "contact_cards": contact_cards,
        "basket_count": basket_count,
        "basket_cost": basket_cost,
    }
    return render(request, "mainapp/contact.html", content)
