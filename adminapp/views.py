from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, render
from django.template.loader import render_to_string
from django.urls import reverse

from adminapp.forms import CategoryCreationForm, ShopUserAdminCreationForm, UserAdminEditForm
from authnapp.models import ShopUser
from mainapp.models import Category, Product


@user_passes_test(lambda x: x.is_staff)
def main(request):
    return HttpResponseRedirect(reverse("admin:users"))


# CRUD for USERS


@user_passes_test(lambda x: x.is_staff)
def users(request, username=None):
    title = "Список пользователей"
    if username:
        users = ShopUser.objects.filter(username__contains=username)
        content = {
            "title": title,
            "users": users,
            "media_url": settings.MEDIA_URL,
        }
        result = render_to_string(
            "adminapp/includes/inc_users_list.html", content)
        return JsonResponse({"result": result})
    users = ShopUser.objects.all()
    content = {
        "title": title,
        "users": users,
        "media_url": settings.MEDIA_URL,
        "active": "users",
    }
    return render(request, "adminapp/users.html", content)


@user_passes_test(lambda x: x.is_staff)
def user(request, pk):
    user = ShopUser.objects.get(pk=pk)
    title = f"Пользователь {user.username}"
    content = {
        "title": title,
        "user": user,
        "media_url": settings.MEDIA_URL,
        "active": "users",
    }
    return render(request, "adminapp/user_profile.html", content)


@user_passes_test(lambda x: x.is_staff)
def create_user(request):
    title = "Создание нового пользователя"
    form = ShopUserAdminCreationForm()
    content = {
        "title": title,
        "form": form,
        "media_url": settings.MEDIA_URL,
        "active": "users",
    }
    return render(request, "adminapp/create_user.html", content)


@user_passes_test(lambda x: x.is_staff)
def user_update(request, pk):
    user_to_update = ShopUser.objects.get(pk=pk)
    title = f"Пользователь {user_to_update.username}"

    if request.method == "POST":
        form = UserAdminEditForm(
            request.POST, request.FILES, instance=user_to_update)
        if form.is_valid():
            form.save()
            return user(request, pk)
    else:
        form = UserAdminEditForm(instance=user_to_update)
        content = {
            "title": title,
            "form": form,
            "media_url": settings.MEDIA_URL,
            "user": user_to_update,
            "active": "users",
        }
        return render(request, "adminapp/user_edit.html", content)


@user_passes_test(lambda x: x.is_staff)
def users_delete(request, pk):
    del_user = ShopUser.objects.get(pk=pk)
    if del_user.is_active:
        del_user.is_active = False
        del_user.save()
    else:
        del_user.is_active = True
        del_user.save()
    status = str(del_user.is_active)
    return JsonResponse({"status": status})


# CRUD for CATEGORY

@user_passes_test(lambda x: x.is_staff)
def category(request):
    title = "Категории"
    categorys = Category.objects.all()
    content = {
        "title": title,
        "categorys": categorys,
        "media_url": settings.MEDIA_URL,
        "active": "category",
    }
    return render(request, "adminapp/category.html", content)


@user_passes_test(lambda x: x.is_staff)
def create_category(request):
    title = "Создать категорию"

    if request.method == "POST":
        form = CategoryCreationForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse('admin:category'))

    form = CategoryCreationForm()
    content = {
        "title": title,
        "form": form,
        "media_url": settings.MEDIA_URL,
        "active": "category",
    }
    return render(request, "adminapp/category_create.html", content)


@user_passes_test(lambda x: x.is_staff)
def category_view(request, pk):
    title = "Категория"
    if pk == 1:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category_id=pk)
    content = {
        "title": title,
        "products": products,
        "media_url": settings.MEDIA_URL,
        "active": "category",
    }
    return render(request, "adminapp/category_view.html", content)


@user_passes_test(lambda x: x.is_staff)
def category_edit(request, pk):
    edit_category = Category.objects.get(pk=pk)
    title = f"Категория {edit_category.title}"
    if request.method == "POST":
        form = CategoryCreationForm(
            request.POST, request.FILES, instance=edit_category)
        form.save()
        return HttpResponseRedirect(reverse('admin:category'))

    form = CategoryCreationForm(instance=edit_category)
    content = {
        "title": title,
        "form": form,
        "media_url": settings.MEDIA_URL,
        "category": edit_category,
        "active": "category",
    }
    return render(request, "adminapp/category_edit.html", content)


@user_passes_test(lambda x: x.is_staff)
def category_delete(request, pk):
    category_to_delete = Category.objects.get(pk=pk)
    category_to_delete.is_active = False if category_to_delete.is_active else True
    category_to_delete.save()
    status = category_to_delete.is_active
    return JsonResponse({"status": str(status)})
