from basketapp.models import Basket


def basket_processor(request):
    basket_items = []
    basket_count = []
    basket_cost = []
    if request.user.is_authenticated:
        basket_items = Basket.objects.filter(user=request.user)
        basket_count = Basket.product_count(request.user)
        basket_cost = Basket.total_cost(request.user)
    content = {
        "basket_items": basket_items,
        "basket_count": basket_count,
        "basket_cost": basket_cost,
    }
    return content
