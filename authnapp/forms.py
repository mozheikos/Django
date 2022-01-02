from django.contrib.auth.forms import AuthenticationForm
from .models import ShopUser


class ShopUserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs) -> None:
        super(ShopUserLoginForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = ShopUser
        fields = ("username", "password")
