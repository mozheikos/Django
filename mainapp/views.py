import json
from random import randint

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
    basket_count = []
    basket_cost = []
    if request.user.is_authenticated:
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


def products(request, product_pk=None, category_pk=0):
    title = "продукты"
    links = Category.objects.all()
    hot = False
    product_large = None
    if product_pk:
        product_large = Product.objects.get(pk=product_pk)
        same_products = Product.objects.filter(
            category_id=product_large.category_id).exclude(pk=product_pk)
    else:
        if not category_pk:
            product_large = Product.objects.get(
                pk=randint(1, Product.objects.all().count()))
            category_pk = product_large.category_id
            same_products = Product.objects.filter(
                category_id=product_large.category_id).exclude(pk=product_pk)
            hot = True
        elif category_pk == 1:
            same_products = Product.objects.all()
        else:
            same_products = Product.objects.filter(category_id=category_pk)

    basket_count = []
    basket_cost = []
    if request.user.is_authenticated:
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
        'hot': hot,
    }
    if category_pk:
        print(f"User select category: {category_pk}")
    return render(request, "mainapp/products.html", content)


def contact(request):
    title = "о нас"

    basket_count = []
    basket_cost = []
    if request.user.is_authenticated:
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
