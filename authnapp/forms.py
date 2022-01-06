from django.contrib.auth import forms, models
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm

from .models import ShopUser


class ShopUserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs) -> None:
        super(ShopUserLoginForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = ShopUser
        fields = ("username", "password")


class ShopUserEditForm(UserChangeForm):
    def __init__(self, *args, **kwargs) -> None:
        super(ShopUserEditForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    """Валидатор картинки. self - объект из формы, cleaned_data - содержимое 
    формы. Оттуда достаем поле аватар - название файла с расширением. Отрезаем
    расширение и проверяем, относится ли оно к поддерживаемым типам. Если да - 
    возвращаем путь: каталог + имя файла, если нет - возвращаем None"""

    def clean_avatar(self):
        allowed_types = ['jpg', 'jpeg', 'png', 'svg', 'bmp']
        ava = self.cleaned_data['avatar']
        if ava:
            ava = str(ava).rsplit('.', 1)
            if not ava[1] or ava[1] not in allowed_types:
                raise forms.ValidationError('Не поддерживаемый тип файла')
        return 'users_avatars/' + '.'.join(ava) if ava else None

    class Meta:
        model = ShopUser
        fields = ("username", "first_name",
                  "last_name", "email", "age", "avatar")


class ShopUserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs) -> None:
        super(ShopUserRegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean_age(self):
        age = self.cleaned_data["age"]
        if age and age < 18:
            raise forms.ValidationError("Вы слишком молоды")
        return age

    class Meta:
        model = ShopUser
        fields = ("username", "password1", "password2", "age")