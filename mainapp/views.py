import json
from random import choice, randint

from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils import timezone

from basketapp.models import Basket

from .models import Category, Contact, Product


def get_controller_data(file_name):
    with open(f"data_json/{file_name}", "r") as f:
        data = json.load(f)
    return data


def get_random_product():
    products = Product.objects.filter(is_active=True, category__is_active=True)
    return choice(products)


def main(request):
    title = "Главная"

    products = Product.objects.filter(is_active=True, category__is_active=True)

    content = {
        "title": title,
        "products": products,
        "media_url": settings.MEDIA_URL,
    }
    return render(request, "mainapp/index.html", content)


def products(request, product_pk=None, category_pk=0, page=1):
    category_pk = int(category_pk)
    page = int(page)
    title = "продукты"
    links = Category.objects.filter(is_active=True)
    hot = False
    product_large = None
    if product_pk:
        product_pk = int(product_pk)
        product_large = Product.objects.get(pk=product_pk)
        same_products = Product.objects.filter(category_id=product_large.category_id, is_active=True).exclude(
            pk=product_pk
        )
    else:
        if not category_pk:
            product_large = get_random_product()
            category_pk = product_large.category_id
            same_products = Product.objects.filter(category_id=product_large.category_id, is_active=True).exclude(
                pk=product_large.pk
            )
            hot = True
        elif category_pk == 1:
            same_products = Product.objects.filter(is_active=True, category__is_active=True)
        else:
            same_products = Product.objects.filter(category_id=category_pk, is_active=True)

    paginator = Paginator(same_products, 3)
    products_paginator = paginator.page(page)

    content = {
        "title": title,
        "links": links,
        "same_products": products_paginator,
        "product_large": product_large,
        "media_url": settings.MEDIA_URL,
        "category": category_pk,
        "hot": hot,
    }
    if category_pk:
        print(f"User select category: {category_pk}")
    return render(request, "mainapp/products.html", content)


def contact(request):
    title = "о нас"

    contact_cards = Contact.objects.all()
    today = timezone.now()

    content = {
        "title": title,
        "visit_date": today,
        "contact_cards": contact_cards,
    }
    return render(request, "mainapp/contact.html", content)
