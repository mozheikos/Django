from dataclasses import fields
from webbrowser import get
from mainapp.models import Category, Product
from authnapp.models import ShopUser
from adminapp.forms import CategoryCreationForm, ShopUserAdminCreationForm, UserAdminEditForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse, request
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView


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
        'category': pk
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


# products crud
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'adminapp/create_product.html'

    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_pk = self.kwargs["category"]
        context['form'].fields['category'].initial = Category.objects.get(
            pk=cat_pk)
        context['form'].fields['category'].queryset = Category.objects.filter(
            pk__gt=1, is_active=True)
        context['category'] = cat_pk
        context["title"] = f'Добавить продукт'
        context["media_url"] = settings.MEDIA_URL
        context['active'] = 'category'
        ProductCreateView.success_url = reverse_lazy(
            'admin:category_view', args=[cat_pk])
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'adminapp/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Продукты'
        context["media_url"] = settings.MEDIA_URL
        context['active'] = 'category'
        return context


class ProductEditView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'adminapp/product_edit.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(ProductEditView, self).get_context_data(**kwargs)
        context["title"] = f'Редактировать {self.kwargs["pk"]}'
        context["media_url"] = settings.MEDIA_URL
        context['active'] = 'category'
        ProductEditView.success_url = reverse_lazy(
            f'admin:product', args=[self.kwargs["pk"]])
        return context
