from django.conf import settings
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render

from basketapp.models import Basket
from mainapp.models import Product


def basket(request):
    title = f"Корзина пользователя: {request.user.username}"
    basket_items = Basket.objects.filter(user=request.user)
    basket_count = Basket.product_count(request.user)
    basket_cost = Basket.total_cost(request.user)
    row = 0
    content = {
        "title": title,
        "basket_items": basket_items,
        "basket_count": basket_count,
        "basket_cost": basket_cost,
        "media_url": settings.MEDIA_URL,
        "row": row,
    }
    return render(request, "basketapp/basket.html", content)

    # content = {}
    # return render(request, "basketapp/basket.html", content)
    # return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def add_to_basket(request, pk):
    product = get_object_or_404(Product, pk=pk)
    quantity = int(request.POST["quant"])
    if request.user.is_authenticated:
        basket, created = Basket.objects.get_or_create(
            user=request.user, product=product, defaults={"quantity": quantity}
        )
    if not created:
        basket.quantity += quantity
        basket.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def remove_from_basket(request, pk):
    Basket.objects.get(pk=pk).delete()
    return basket(request)
    # return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
