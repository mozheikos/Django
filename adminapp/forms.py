# from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from django import forms
from django.forms.models import ModelForm

from authnapp.forms import ShopUserEditForm, ShopUserRegisterForm
from authnapp.models import ShopUser
from mainapp.models import Category


class ShopUserAdminCreationForm(ShopUserRegisterForm):
    def __init__(self, *args, **kwargs) -> None:
        super(ShopUserAdminCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form_field"

    class Meta:
        model = ShopUser
        fields = ("username", "password1", "password2",
                  "age", "is_staff", "is_superuser")


class UserAdminEditForm(ShopUserEditForm):
    def __init__(self, *args, **kwargs) -> None:
        super(UserAdminEditForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form_field"

    class Meta:
        model = ShopUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "age",
            "avatar",
            "is_active",
            "is_staff",
            "is_superuser",
        )


class CategoryCreationForm(ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super(CategoryCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form_field"
        self.fields['discount'].widget.attrs["step"] = 5

    class Meta:
        model = Category
        fields = ("title", "description", "discount")
