from django.conf import settings
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from basketapp.models import Basket
from mainapp.models import Product


@login_required
def basket(request):
    title = f"Корзина пользователя: {request.user.username}"
    basket_items = []
    basket_count = []
    basket_cost = []
    basket_items = Basket.objects.filter(user=request.user)
    basket_count = Basket.product_count(request.user)
    basket_cost = Basket.total_cost(request.user)
    content = {
        "title": title,
        "basket_items": basket_items,
        "basket_count": basket_count,
        "basket_cost": basket_cost,
        "media_url": settings.MEDIA_URL,
    }
    return render(request, "basketapp/basket.html", content)


@login_required
def add_to_basket(request, category_pk, pk):
    """Так как в моем случае добавление в корзину реализовано через форму, для 
    того, чтобы можно было добавить не одну, а сразу несколько единиц товара,
    в случае редиректа из login-формы прилетает GET-запрос и все ломается. Думал,
    как обойти, собирался уже в логине резать адрес редиректа и добавлять условия,
    но решил, что лучше так, потому что это решает и еще один момент, который
    мне не нравился: я хочу, чтобы после логина товар автоматически не добавлялся,
    а все-таки просто возвращало на страницу с тем же товаром. Ведь после логина
    может быть возможность, допустим, ввода промокода и получения скидки или чтото
    еще подобное"""
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        quantity = int(request.POST["quant"])
        basket, created = Basket.objects.get_or_create(
            user=request.user, product=product, defaults={"quantity": quantity}
        )
        if not created:
            basket.quantity += quantity
            basket.save()

    next_page = request.path.replace('/basket/add/', '/products/')
    return HttpResponseRedirect(next_page)


"""Так как поле изменения заказанного количества и кнопка удаления позиции нахо-
дятся внутри корзины, а корзину может увидеть только зарегистрированный и зало-
гиненый пользователь - ставить декоратор @login_required на функции удаления и
редактирования не вижу смысла. Они априори могут быть вызваны только пользователем,
авторизовавшимся на сайте"""


def remove_from_basket(request, pk):
    Basket.objects.get(pk=pk).delete()
    return basket(request)


def edit_quantity(request, pk, quantity):
    edit_elem = Basket.objects.get(pk=int(pk))
    edit_elem.update(quantity=int(quantity))
    basket_count = Basket.product_count(user=request.user)
    basket_cost = Basket.total_cost(request.user)
    product_cost = edit_elem.product_cost
    return JsonResponse({'quantity': quantity, 'basket_count': basket_count, 'basket_cost': basket_cost, 'product_cost': product_cost})
