from django.shortcuts import HttpResponseRedirect, get_object_or_404, render

from basketapp.models import Basket
from mainapp.models import Product


def basket(request):
    #content = {}
    # return render(request, "basketapp/basket.html", content)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def add_to_basket(request, pk):
    product = get_object_or_404(Product, pk=pk)
    quantity = int(request.POST['quant'])
    basket = Basket.objects.filter(
        user=request.user, product=product).first()
    if not basket:
        basket = Basket(user=request.user, product=product, quantity=quantity)
    else:
        basket.quantity += quantity
    if request.user.is_authenticated:
        basket.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def remove_from_basket(request, pk):
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
