from django.urls import path, re_path

import adminapp.views as adminapp

from .apps import AdminappConfig

app_name = AdminappConfig.name

urlpatterns = [
    # admin_mainpage
    re_path(r"^$", adminapp.main, name="users"),
    # admin_users_CRUD
    re_path(r"^users_create/$", adminapp.UserCreateView.as_view(), name="users_create"),
    re_path(r"^users/$", adminapp.UsersListView.as_view(), name="users"),
    re_path(r"^user_view/(?P<pk>\d+)/$", adminapp.UserDetailView.as_view(), name="user_view"),
    re_path(r"^user_update/(?P<pk>\d+)/$", adminapp.UserUpdateView.as_view(), name="user_update"),
    # path("users/user_delete/<int:pk>/",
    #     adminapp.UserDeleteNotView.as_view(), name="user_delete"),
    re_path(r"^users/user_delete/(?P<pk>\d+)/$", adminapp.UserDeleteAjax.as_view(), name="user_delete"),
    # admin_category_CRUD
    re_path(r"^category/$", adminapp.category, name="category"),
    re_path(r"^category_create/$", adminapp.create_category, name="category_create"),
    re_path(r"^category_view/(?P<pk>\d+)/$", adminapp.category_view, name="category_view"),
    re_path(r"^category_edit/(?P<pk>\d+)/$", adminapp.category_edit, name="category_edit"),
    re_path(r"^category/category_delete/(?P<pk>\d+)/$", adminapp.category_delete, name="category_delete"),
    # admin_product_CRUD
    re_path(r"^product/(?P<pk>\d+)/$", adminapp.ProductDetailView.as_view(), name="product"),
    re_path(r"^product_update/(?P<pk>\d+)/$", adminapp.ProductEditView.as_view(), name="product_update"),
    re_path(r"^product_create/(?P<category>\d+)/$", adminapp.ProductCreateView.as_view(), name="product_create"),
    re_path(r"^product_delete/(?P<pk>\d+)/$", adminapp.ProductDeleteNotView.as_view(), name="product_delete"),
]
