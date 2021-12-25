import json

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
same_products = [
    {
        "name": "Отличный стул",
        "desc": "На таком стуле сидеть...на люстру больше похоже",
        "image_src": "product-11.jpg",
        "alt": "продукт 11"
    },

    {
        "name": "Стул повышенного качества",
        "desc": "Комфортно.",
        "image_src": "product-21.jpg",
        "alt": "продукт 21"
    },

    {
        "name": "Стул премиального качества",
        "desc": "Только это лампа, а так стул.",
        "image_src": "product-31.jpg",
        "alt": "продукт 31",
    },
]
contact_cards = [
    {'city': 'Москва',
     'phone': '+7-495-555-55-55',
     'mail': 'moscow@info.ru',
     'address': 'ул. 3-я Строителей, д. 25, кв. 12'
     },

    {'city': 'Ленинград',
     'phone': '+7-812-312-12-12',
     'mail': 'spb@info.ru',
     'address': 'ул. 3-я Строителей, д. 25, кв. 12'
     },

    {'city': 'Белгород',
     'phone': '+7-4722-22-12-32',
     'mail': 'belgorod@info.ru',
     'address': 'ул. Ленина, д. 1, оф. 12'
     },
]
links = [
    {'href': 'all', 'cat_name': 'Все'},
    {'href': 'home', 'cat_name': 'Дом'},
    {'href': 'office', 'cat_name': 'Офис'},
    {'href': 'modern', 'cat_name': 'Модерн'},
    {'href': 'classic', 'cat_name': 'Классика'}
]
files = [
    (products, 'main_products.json'),
    (same_products, 'same_products.json'),
    (contact_cards, 'cities.json'),
    (links, 'links.json')
]

for item in files:
    with open(item[1], 'w') as f:
        json.dump(item[0], f)
