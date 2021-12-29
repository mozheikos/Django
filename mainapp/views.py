from django.conf import settings
from django.shortcuts import render
import datetime

from .models import Product, Category
import json


def get_controller_data(file_name):
    with open(f'data_json/{file_name}', 'r') as f:
        data = json.load(f)
    return data


def main(request):
    title = 'Главная'

    products = Product.objects.all()

    content = {'title': title, 'products': products,
               "media_url": settings.MEDIA_URL}
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    title = "продукты"
    links = Category.objects.all()
    same_products = Product.objects.all()
    content = {"title": title, "links": links,
               "same_products": same_products, "media_url": settings.MEDIA_URL}
    if pk:
        print(f'User select category: {pk}')
    return render(request, "mainapp/products.html", content)


def contact(request):
    title = "о нас"

    contact_cards = get_controller_data('cities.json')
    today = datetime.datetime.now()

    content = {"title": title, "visit_date": today,
               'contact_cards': contact_cards}
    return render(request, "mainapp/contact.html", content)
