from cProfile import label
from django import forms

from ordersapp.models import Order, OrderItem
from mainapp.models import Product


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Order
        exclude = ("user",)


class OrderItemForm(forms.ModelForm):
    price = forms.CharField(label="Цена", required=False)

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.get_items().select_related()
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = OrderItem
        exclude = ()
