from django.shortcuts import render
import datetime


def main(request):
    title = 'Главная'
    products = [
        {
            'name': "Отличный стул",
            'desc': "Расположись комфортно",
            'image_src': "product-1.jpg",
            'image_href': "/product/1/",
            'alt': "стул 1"
        },
        {
            'name': "Еще один хороший стул",
            'desc': "Вставать не захочешь",
            'image_src': "product-2.jpg",
            'image_href': "/product/2/",
            'alt': "стул 2"
        }
    ]
    content = {'title': title, 'products': products}
    return render(request, 'mainapp/index.html', content)


def products(request):
    title = "продукты"
    content = {"title": title}
    return render(request, "mainapp/products.html", content)


def contact(request):
    title = "о нас"
    visit_date = datetime.datetime.now()
    content = {"title": title, "visit_date": visit_date}
    return render(request, "mainapp/contact.html", content)
