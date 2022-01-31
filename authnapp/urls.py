from django.urls import path, re_path

import authnapp.views as authnapp

app_name = "authnapp"

urlpatterns = [
    re_path(r"^login/$", authnapp.login, name="login"),
    re_path(r"^logout/$", authnapp.logout, name="logout"),
    re_path(r"^profile/$", authnapp.user_profile, name="profile"),
    re_path(r"^register/$", authnapp.register, name="register"),
    re_path(r"^user_edit/$", authnapp.user_edit, name="user_edit"),
    re_path(r"^verify/(?P<user_id>\d+)/(?P<user_auth_key>\w+)/$", authnapp.verify, name="verify"),
]
