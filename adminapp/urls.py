from django.urls import path

import adminapp.views as adminapp

from .apps import AdminappConfig

app_name = AdminappConfig.name

urlpatterns = [
    # admin_mainpage
    path("", adminapp.main, name="users"),
    # admin_users_CRUD
    path("users_create/", adminapp.create_user, name="users_create"),
    path("users/", adminapp.users, name="users"),
    path("users/<username>/", adminapp.users, name="users"),
    path("user_view/<int:pk>/", adminapp.user, name="user_view"),
    path("user_update/<int:pk>/", adminapp.user_update, name="user_update"),
    path("users/user_delete/<int:pk>/",
         adminapp.users_delete, name="user_delete"),
    # admin_category_CRUD
    path("category/", adminapp.category, name="category"),
    path("category_create", adminapp.create_category, name="category_create"),
    path("category_view/<int:pk>", adminapp.category_view, name="category_view"),
    path("category_edit/<int:pk>", adminapp.category_edit, name="category_edit"),
    path("category/category_delete/<int:pk>",
         adminapp.category_delete, name="category_delete"),
    # admin_product_CRUD
    path('product/<int:pk>',
         adminapp.ProductDetailView.as_view(), name='product'),
    path('product_update/<int:pk>',
         adminapp.ProductEditView.as_view(), name='product_update'),
    path('product_create/<int:category>',
         adminapp.ProductCreateView.as_view(), name='product_create')
]
