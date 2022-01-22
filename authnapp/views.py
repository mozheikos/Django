import re

from django.conf import settings
from django.contrib import auth
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse

from adminapp.forms import ShopUserAdminCreationForm
from authnapp.forms import ShopUserEditForm, ShopUserLoginForm, ShopUserRegisterForm
from authnapp.models import ShopUser


def login(request):
    title = "Вход в систему"

    next_page = request.GET["next"] if "next" in request.GET.keys() else ""
    login_form = ShopUserLoginForm(data=request.POST or None)
    if request.method == "POST" and login_form.is_valid():
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if "next_page" in request.POST.keys():
                return HttpResponseRedirect(request.POST["next_page"])
            return HttpResponseRedirect(reverse("main"))

    content = {"title": title, "login_form": login_form, "next_page": next_page}
    return render(request, "authnapp/login.html", content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("main"))


def user_profile(request):
    title = "Профиль пользователя"
    context = {
        "title": title,
        "media_url": settings.MEDIA_URL,
    }
    return render(request, "authnapp/profile.html", context)


def register(request):
    title = "регистрация"

    if request.method == "POST":
        if request.META.get("HTTP_REFERER").find("admin/users_create/") != -1:
            register_form = ShopUserAdminCreationForm(request.POST, request.FILES)
        else:
            register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            register_form.save()
            if request.META.get("HTTP_REFERER").find("admin/users_create/") != -1:
                return HttpResponseRedirect(reverse("admin:users"))
            return HttpResponseRedirect(reverse("auth:login"))
    else:
        register_form = ShopUserRegisterForm()

    content = {"title": title, "register_form": register_form}
    return render(request, "authnapp/register.html", content)


def user_edit(request):
    title = "Профиль пользователя"
    if request.method == "POST":
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse("auth:profile"))
    else:
        edit_form = ShopUserEditForm(instance=request.user)

    context = {"title": title, "edit_form": edit_form, "media_url": settings.MEDIA_URL}
    return render(request, "authnapp/edit.html", context)
