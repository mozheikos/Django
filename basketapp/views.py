from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.db.models import F
from mainapp.models import db_profile_by_type
from django.db import connection

from basketapp.models import Basket
from mainapp.models import Product


@login_required
def basket(request):
    title = f"Корзина пользователя: {request.user.username}"

    back = request.META.get("HTTP_REFERER")
    content = {
        "title": title,
        "media_url": settings.MEDIA_URL,
        "back": back,
    }
    return render(request, "basketapp/basket.html", content)


@login_required
def add_to_basket(request, category_pk, pk):
    """using function: db_profile_by_type(Basket, "UPDATE", connection.queries) ->
    stdout: 
        [21/Feb/2022 19:07:25] "GET /products/5/8/ HTTP/1.1" 200 18131

        db_profile UPDATE for <class 'basketapp.models.Basket'>:

        UPDATE "basketapp_basket" SET "user_id" = 1, "product_id" = 8,
        "quantity" = ("basketapp_basket"."quantity" + 3),
        "add_datetime" = '2022-02-21 19:07:24.285066'
        WHERE "basketapp_basket"."id" = 8

    """

    pk = int(pk)
    if request.method == "POST":
        product = get_object_or_404(Product, pk=pk)
        quantity = int(request.POST["quant"])
        basket, created = Basket.objects.get_or_create(
            user=request.user, product=product, defaults={"quantity": quantity}
        )
        if not created:
            basket.quantity = F("quantity") + quantity
            basket.save()

    next_page = request.path.replace("/basket/add/", "/products/")
    return HttpResponseRedirect(next_page)


def remove_from_basket(request, pk):
    pk = int(pk)
    Basket.objects.get(pk=pk).delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def edit_quantity(request, pk, quantity):
    pk = int(pk)
    quantity = int(quantity)
    edit_elem = Basket.objects.get(pk=int(pk))
    edit_elem.quantity = int(quantity)
    edit_elem.save()
    _, basket_count, basket_cost = Basket.product_count(user=request.user)
    product_cost = edit_elem.product_cost
    return JsonResponse(
        {"quantity": quantity, "basket_count": basket_count,
            "basket_cost": basket_cost, "product_cost": product_cost}
    )
