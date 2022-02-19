import json
from os import link
from random import choice
from django.core.cache import cache
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils import timezone
from .models import Category, Contact, Product


def get_links():
    if settings.LOW_CACHE:
        key = "menu_links"
        links = cache.get(key)
        if links is None:
            links = Category.objects.filter(is_active=True).order_by("id")
            cache.set(key, links)
        return links
    else:
        return Category.objects.filter(is_active=True).order_by("id")


def get_product(pk):
    if settings.LOW_CACHE:
        key = f"product_{pk}"
        product = cache.get(key)
        if product is None:
            product = Product.objects.get(pk=pk)
            cache.set(key, product)
        return product
    else:
        return Product.objects.get(pk=pk)


def get_all_active_products(*args):
    if not len(args):
        order = ("id", )
    else:
        order = args
    if settings.LOW_CACHE:
        key = "all_active_products"
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(
                is_active=True, category__is_active=True).order_by(*order)
            cache.set(key, products)
        return products
    else:
        category = Category.objects.filter(
            id__gt=1, is_active=True).order_by("id")
        products = []
        for item in category:
            _products = item.category_products.order_by(*order)
            products.extend(_products)
        return products


def get_category_products(category_pk, *args):
    if not len(args):
        order = ("id", )
    else:
        order = args

    if settings.LOW_CACHE:
        key = f"products_category_{category_pk}"
        products = cache.get(key)
        if products is None:
            category = Category.objects.get(pk=category_pk)
            products = category.category_products.order_by(*order)
            cache.set(key, products)
        return products
    else:
        category = Category.objects.get(pk=category_pk)
        products = category.category_products.order_by(*order)
        return products


def get_controller_data(file_name):
    with open(f"data_json/{file_name}", "r") as f:
        data = json.load(f)
    return data


def get_random_product():
    products = get_all_active_products()
    product = choice(products)
    return (product, [x for x in products if x.category_id == product.category_id and x.id != product.id])


def main(request):
    title = "Главная"

    products = get_all_active_products("category_id", "name")

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
    links = get_links()
    hot = False
    product_large = None
    if product_pk:
        product_pk = int(product_pk)
        product_large = get_product(product_pk)
        same_products = get_category_products(
            product_large.category_id, 'price').exclude(pk=product_pk)
    else:
        if not category_pk:
            product_large, same_products = get_random_product()
            category_pk = product_large.category_id
            hot = True
        else:
            if category_pk == 1:
                same_products = get_all_active_products("category_id", "name")
            else:
                same_products = get_category_products(category_pk, "name")

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
