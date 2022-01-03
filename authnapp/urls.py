from django.urls import path

import authnapp.views as authnapp

app_name = "authnapp"

urlpatterns = [
    path("login/", authnapp.login, name="login"),
    path("logout/", authnapp.logout, name="logout"),
    path("profile/", authnapp.user_profile, name="profile"),
    path("register/", authnapp.register, name="register"),
    path("user_edit/", authnapp.user_edit, name="user_edit"),
]
