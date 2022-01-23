from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='age')
def age(age):
    age = int(age)
    age_ = age % 100
    if 10 < age_ < 20 or age_ % 10 > 4 or age_ % 10 == 0:
        return f'{age} лет'
    elif age % 10 > 1:
        return f'{age} года'
    return f'{age} год'
