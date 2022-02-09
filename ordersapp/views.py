from dataclasses import fields

from django.db import transaction
from django.dispatch import receiver
from django.db.models.signals import pre_delete, pre_save, post_save
from django.forms import inlineformset_factory
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views.generic.detail import DetailView

from basketapp.models import Basket
from ordersapp.forms import OrderItemForm
from ordersapp.models import Order, OrderItem


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user_id=self.request.user.pk)


class OrderItemsCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy("ordersapp:orders_list")

    def get_context_data(self, **kwargs):
        data = super(OrderItemsCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(
            Order, OrderItem, form=OrderItemForm, extra=0)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.get_items(self.request.user)
            if len(basket_items):
                OrderFormSet = inlineformset_factory(
                    Order, OrderItem, form=OrderItemForm, extra=len(basket_items))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial["product"] = basket_items[num].product
                    form.initial["quantity"] = basket_items[num].quantity
                    form.initial["price"] = basket_items[num].product.price
            else:
                OrderFormSet = inlineformset_factory(
                    Order, OrderItem, form=OrderItemForm, extra=1)
                formset = OrderFormSet()

        data["orderitems"] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context["orderitems"]

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            # Delete items in basket after order creating only
            Basket.objects.filter(user=self.request.user).delete()

        # Delete empty order
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemsCreate, self).form_valid(form)


class OrderRead(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderRead, self).get_context_data(**kwargs)
        context["title"] = "заказ/просмотр"
        return context


class OrderItemsUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy("ordersapp:orders_list")

    def get_context_data(self, **kwargs):
        data = super(OrderItemsUpdate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(
            Order, OrderItem, form=OrderItemForm, extra=0)
        if self.request.POST:
            data["orderitems"] = OrderFormSet(
                self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial["price"] = form.instance.product.price
            data["orderitems"] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context["orderitems"]

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # Delete empty order
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemsUpdate, self).form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy("ordersapp:orders_list")


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse("ordersapp:orders_list"))


# I update product.count only by OrderItem signal, because adding product to basket
# is not a purchase
@receiver(pre_save, sender=OrderItem)
def product_count_update_save(instance, sender, **kwargs):
    quantity_delta = instance.quantity
    if instance.pk:
        quantity_delta -= sender.get_item(instance.pk).quantity
    instance.product.count -= quantity_delta
    instance.product.save()


@receiver(pre_delete, sender=OrderItem)
def product_count_update_delete(instance, sender, **kwargs):
    instance.product.count += instance.quantity
    instance.product.save()

# Deleting orderitem if quantity = 0


@receiver(post_save, sender=OrderItem)
def del_zero_quant(instance, sender, **kwargs):
    product = OrderItem.objects.filter(pk=instance.pk)
    if len(product):
        if int(instance.quantity) == 0:
            sender.get_item(instance.pk).delete()
