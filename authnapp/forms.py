from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm

from .models import ShopUser, ShopUserProfile


class ShopUserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs) -> None:
        super(ShopUserLoginForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form_field"

    class Meta:
        model = ShopUser
        fields = ("username", "password")


class ShopUserEditForm(UserChangeForm):
    def __init__(self, *args, **kwargs) -> None:
        super(ShopUserEditForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form_field"

    """Валидатор картинки. self - объект из формы, cleaned_data - содержимое 
    формы. Оттуда достаем поле аватар - название файла с расширением. Отрезаем
    расширение и проверяем, относится ли оно к поддерживаемым типам. Если да - 
    возвращаем путь: каталог + имя файла, если нет - возвращаем None"""

    def clean_avatar(self):
        allowed_types = ["image/jpg", "image/jpeg",
                         "image/png", "image/svg", "image/bmp"]
        if ["avatar"] in self.changed_data:
            ava = self.cleaned_data["avatar"]
        else:
            ava = None
        if ava:
            if ava.content_type not in allowed_types:
                raise forms.ValidationError("Не поддерживаемый тип файла")
        else:
            ava = self.cleaned_data["avatar"] if self.cleaned_data["avatar"] else "users_avatars/default.jpg"
        return ava

    class Meta:
        model = ShopUser
        fields = ("username", "first_name",
                  "last_name", "email", "age", "avatar")


class ShopUserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs) -> None:
        super(ShopUserRegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages['required'] = f"Поле {field.label} обязательно для заполнения"
            field.widget.attrs["class"] = "form_field"

    def save(self):
        user = super(ShopUserRegisterForm, self).save()

        user.is_active = False
        user.get_auth_key()
        user.save()
        return user

    def clean_age(self):
        age = self.cleaned_data["age"]
        if age and age < 18:
            raise forms.ValidationError("Вы слишком молоды")
        return age

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not email:
            raise forms.ValidationError(
                "Поле e-mail обязательно для заполнения")
        return email

    class Meta:
        model = ShopUser
        fields = ("username", "email", "password1", "password2", "age")


class ShopUserProfileEditForm(forms.ModelForm):
    class Meta:
        model = ShopUserProfile
        fields = ("tagline", "aboutMe", "interests", "gender")

    def __init__(self, *args, **kwargs):
        super(ShopUserProfileEditForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form_field"
