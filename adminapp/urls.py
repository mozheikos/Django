from django.urls import path

from .apps import AdminappConfig

import adminapp.views as adminapp

app_name = AdminappConfig.name

urlpatterns = [
    # admin_mainpage
    path('', adminapp.main, name='main'),
    # admin_users_CRUD
    path('users_create/', adminapp.create_user, name='users_create'),
    path('users/', adminapp.users, name='users'),
    path('users_update', adminapp.users_update, name='users_update'),
    path('users_delete', adminapp.users_delete, name='users_delete'),
]
