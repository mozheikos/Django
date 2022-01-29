from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, request
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from adminapp.forms import CategoryCreationForm, ShopUserAdminCreationForm
from authnapp.models import ShopUser
from mainapp.models import Category, Product


@user_passes_test(lambda x: x.is_staff)
def main(request):
    return HttpResponseRedirect(reverse("admin:users"))


# CRUD for USERS


"""
@user_passes_test(lambda x: x.is_staff)
def users(request, username=None):
    title = "Список пользователей"
    if username:
        users = ShopUser.objects.filter(
            username__contains=username) if username != "all" else ShopUser.objects.all()
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
    return render(request, "adminapp/users.html", content)"""


class UsersListView(LoginRequiredMixin, ListView):
    model = ShopUser
    template_name = "adminapp/users.html"

    def get_context_data(self, **kwargs):
        context = super(UsersListView, self).get_context_data(**kwargs)
        context["title"] = "Пользователи"
        context["media_url"] = settings.MEDIA_URL
        context["login_url"] = settings.LOGIN_URL
        context["active"] = "users"
        username = self.kwargs["username"] if "username" in self.kwargs.keys(
        ) else None
        if username:
            self.queryset = ShopUser.objects.filter(
                username__contains=username)
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


"""@user_passes_test(lambda x: x.is_staff)
def user(request, pk):
    user = ShopUser.objects.get(pk=pk)
    title = f"Пользователь {user.username}"
    content = {
        "title": title,
        "user": user,
        "media_url": settings.MEDIA_URL,
        "active": "users",
    }
    return render(request, "adminapp/user_profile.html", content)"""


class UserDetailView(LoginRequiredMixin, DetailView):
    model = ShopUser
    template_name = "adminapp/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Пользователь {self.object.username}"
        context["media_url"] = settings.MEDIA_URL
        context["login_url"] = settings.LOGIN_URL
        context["active"] = "users"
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


"""@user_passes_test(lambda x: x.is_staff)
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
"""


class UserCreateView(LoginRequiredMixin, CreateView):
    model = ShopUser
    template_name = "adminapp/create_user.html"
    form_class = ShopUserAdminCreationForm
    success_url = reverse_lazy("admin:users")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for field in context["form"].fields.keys():
            if context["form"].fields[field].help_text:
                context["form"].fields[field].help_text = None
        context["title"] = f"Добавить пользователя"
        context["media_url"] = settings.MEDIA_URL
        context["login_url"] = settings.LOGIN_URL
        context["active"] = "users"
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = ShopUser
    template_name = "adminapp/user_edit.html"
    fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "age",
        "avatar",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for field in context["form"].fields.keys():
            if context["form"].fields[field].help_text:
                context["form"].fields[field].help_text = None
        context["title"] = f"Редактировать пользователя"
        context["media_url"] = settings.MEDIA_URL
        context["login_url"] = settings.LOGIN_URL
        context["active"] = "users"
        UserUpdateView.success_url = reverse_lazy(
            "admin:user_view", args=[self.object.pk])
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


"""
@user_passes_test(lambda x: x.is_staff)
def user_update(request, pk):
    user_to_update = ShopUser.objects.get(pk=pk)
    title = f"Пользователь {user_to_update.username}"

    if request.method == "POST":
        form = UserAdminEditForm(
            request.POST, request.FILES, instance=user_to_update)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin:user_view', args=[pk]))
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
"""


"""@user_passes_test(lambda x: x.is_staff)
def users_delete(request, pk):
    del_user = ShopUser.objects.get(pk=pk)
    if del_user.is_active:
        del_user.is_active = False
        del_user.save()
    else:
        del_user.is_active = True
        del_user.save()
    status = str(del_user.is_active)
    return JsonResponse({"status": status})"""


"""class UserDeleteNotView(LoginRequiredMixin, DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin:users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)"""


class UserDeleteAjax(LoginRequiredMixin, DeleteView):
    model = ShopUser

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
            status = str(False)
        else:
            self.object.is_active = True
            status = str(True)
        self.object.save()
        return JsonResponse({"status": status})

    def post(self, request, *args: str, **kwargs):
        return self.delete(request, *args, **kwargs)

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

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
        return HttpResponseRedirect(reverse("admin:category"))

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
        "category": pk,
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
        return HttpResponseRedirect(reverse("admin:category"))

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


# products crud
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = "adminapp/create_product.html"
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_pk = self.kwargs["category"]
        context["form"].fields["category"].initial = Category.objects.get(
            pk=cat_pk)
        context["form"].fields["category"].queryset = Category.objects.filter(
            pk__gt=1, is_active=True)
        for field in context["form"].fields.keys():
            context["form"].fields[field].widget.attrs["class"] = "form_field"
        context["category"] = cat_pk
        context["title"] = f"Добавить продукт"
        context["media_url"] = settings.MEDIA_URL
        context["active"] = "category"
        ProductCreateView.success_url = reverse_lazy(
            "admin:category_view", args=[cat_pk])
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "adminapp/product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Продукты"
        context["media_url"] = settings.MEDIA_URL
        context["active"] = "category"
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductEditView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = "adminapp/product_edit.html"
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f'Редактировать {self.kwargs["pk"]}'
        context["media_url"] = settings.MEDIA_URL
        context["active"] = "category"
        cat_pk = self.object.category_id
        context["form"].fields["category"].initial = Category.objects.get(
            pk=cat_pk)
        context["form"].fields["category"].queryset = Category.objects.filter(
            pk__gt=1, is_active=True)
        for field in context["form"].fields.keys():
            context["form"].fields[field].widget.attrs["class"] = "form_field"
        ProductEditView.success_url = reverse_lazy(
            f"admin:product", args=[self.kwargs["pk"]])
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductDeleteNotView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "adminapp/product_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        success_url = reverse_lazy("admin:category_view", args=[
                                   self.object.category_id])
        return HttpResponseRedirect(success_url)

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
