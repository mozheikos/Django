from django.shortcuts import render
import datetime
import json


def get_controller_data(file_name):
    with open(f'data_json/{file_name}', 'r') as f:
        data = json.load(f)
    return data


def main(request):
    title = 'Главная'

    products = get_controller_data('main_products.json')
    content = {'title': title, 'products': products}
    return render(request, 'mainapp/index.html', content)


def products(request):
    title = "продукты"

    links = get_controller_data('links.json')
    same_products = get_controller_data('same_products.json')
    content = {"title": title, "links": links, "same_products": same_products}
    return render(request, "mainapp/products.html", content)


def contact(request):
    title = "о нас"

    contact_cards = get_controller_data('cities.json')
    today = datetime.datetime.now()

    content = {"title": title, "visit_date": today,
               'contact_cards': contact_cards}
    return render(request, "mainapp/contact.html", content)
