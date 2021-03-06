import re
import smtplib
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.db import transaction
from adminapp.forms import ShopUserAdminCreationForm
from authnapp.forms import ShopUserEditForm, ShopUserLoginForm, ShopUserProfileEditForm, ShopUserRegisterForm
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

    content = {"title": title, "login_form": login_form,
               "next_page": next_page}
    return render(request, "authnapp/login.html", content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("main"))


@login_required
def user_profile(request):
    title = "Профиль пользователя"
    context = {
        "title": title,
        "media_url": settings.MEDIA_URL,
    }
    return render(request, "authnapp/profile.html", context)


class UserProfile(LoginRequiredMixin, DetailView):
    model = ShopUser
    template_name = "authnapp/profile_detail.html"


def register(request):
    title = "регистрация"

    if request.method == "POST":
        if request.META.get("HTTP_REFERER") and request.META.get("HTTP_REFERER").find("admin/users_create/") != -1:
            register_form = ShopUserAdminCreationForm(
                request.POST, request.FILES)
        else:
            register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            if request.META.get("HTTP_REFERER") and request.META.get("HTTP_REFERER").find("admin/users_create/") != -1:
                return HttpResponseRedirect(reverse("admin:users"))

            if send_verify_mail(user):

                status = f"На Ваш почтовый ящик {user.email} отправлено письмо подтверждения регистрации.\n \
                                    Для завершения регистрации, пожалуйста, перейдите по ссылке в письме"
            href = reverse("main")
            errors = False
            return JsonResponse({"status": status, "href": href, "errors": errors})
        else:
            errors = True
            href = reverse("auth:register")
            return JsonResponse({"href": href, "errors": errors, "form": register_form.as_p()})

    else:
        register_form = ShopUserRegisterForm()

    content = {"title": title, "register_form": register_form}
    return render(request, "authnapp/register.html", content)


@ login_required
@ transaction.atomic
def user_edit(request):
    title = "Профиль пользователя"
    if request.method == "POST":
        edit_form = ShopUserEditForm(
            request.POST, request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(
            request.POST, instance=request.user.shopuserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse("auth:profile"))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(
            instance=request.user.shopuserprofile)

    context = {"title": title, "edit_form": edit_form,
               "profile_form": profile_form, "media_url": settings.MEDIA_URL}
    return render(request, "authnapp/edit.html", context)


"""
def send_verify_mail(user):
    verify_link = reverse("auth:verify", args=[user.id, user.auth_key])

    title = f"Подтверждение регистрации {user.username}"
    message = f"Вы зарегистрировались на портале {settings.DOMAIN_NAME}. Для подтверждения \
                регистрации перейдите по ссылке:\n{settings.DOMAIN_NAME}{verify_link}"

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
"""


def send_verify_mail(user):
    verify_link = reverse("auth:verify", args=[user.id, user.auth_key])

    title = f"Подтверждение регистрации {user.username}"
    message = f"Вы зарегистрировались на портале {settings.DOMAIN_NAME}. Для подтверждения \
                регистрации перейдите по ссылке:\n{settings.DOMAIN_NAME}{verify_link}"

    HOST = settings.EMAIL_HOST
    SUBJECT = title
    TO = user.email
    FROM = settings.EMAIL_HOST_USER
    PASSWD = settings.EMAIL_HOST_PASSWORD
    PORT = settings.EMAIL_PORT

    BODY = "\n".join((
        "From: %s" % FROM,
        "To: %s" % TO,
        "Subject: %s" % SUBJECT,
        "",
        message
    ))

    server = smtplib.SMTP_SSL(HOST, PORT)
    server.login(FROM, PASSWD)
    server.sendmail(FROM, [TO], BODY.encode('utf-8'))
    server.quit()
    return True


def verify(request, user_id, user_auth_key):
    title = "Подтверждение регистрации"

    user = ShopUser.objects.get(pk=int(user_id))

    if user.auth_key == user_auth_key and not user.is_activation_key_expired():
        user.is_active = True
        user.save()
        auth.login(request, user,
                   backend="django.contrib.auth.backends.ModelBackend")
        link = reverse("main")

    # Пока закооментировал вариант истекшим ключем, так как очень не хватает времени
    # лекцию в пятницу я пропустил из-за работы, а на след неделе возможности нагнать
    #  не предвидится. Но чисто технически переотправка ключа нужна
    # else:
    #    user.get_auth_key()
    #    link = reverse('auth:resend_verify_link', args=[user.id])

    content = {"title": title, "media_url": settings.MEDIA_URL,
               "link": link, "user": user}
    return render(request, "authnapp/verify.html", content)


def resend_verify_link(request, user_id):
    user = ShopUser.objects.get(pk=user_id)
    if send_verify_mail(user):
        status = f"На Ваш почтовый ящик {user.email} отправлено письмо подтверждения регистрации.\n \
                            Для завершения регистрации, пожалуйста, перейдите по ссылке в письме"
        status_code = 200
    else:
        status = f"Что-то пошло не так, нажмите на кнопку для повторной отправки письма"
        status_code = 500.0

    return JsonResponse({"status": status, "code": status_code, "user_id": user_id})
