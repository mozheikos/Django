from django.conf import settings
from django.test import TestCase
from django.test.client import Client

from authnapp.models import ShopUser


class TestUserManagement(TestCase):
    fixtures = [
        "mainapp/fixtures/001_category.json",
        "mainapp/fixtures/002_products.json",
        "mainapp/fixtures/003_contacts.json",
        "authnapp/fixtures/admin.json",
    ]

    def setUp(self) -> None:
        self.client = Client()
        self.user = ShopUser.objects.create_user(
            "tarantino", "tarantini@geekshop.local", "geekbrains")

    def test_user_login(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.context["title"], "Главная")
        self.assertNotContains(response, "tarantino", status_code=200)

        self.client.login(username="tarantino", password="geekbrains")

        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["user"].is_anonymous)
        self.assertEqual(response.context["user"], self.user)

        response = self.client.get("/")
        self.assertContains(response, "tarantino", status_code=200)
        self.assertEqual(response.context["user"], self.user)

    def test_basket_login_redirect(self):
        response = self.client.get("/basket/")
        self.assertEqual(response.url, "/auth/login/?next=/basket/")
        self.assertEqual(response.status_code, 302)

        self.client.login(username="tarantino", password="geekbrains")

        response = self.client.get("/basket/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["basket_items"]), [])
        self.assertEqual(response.context["user"], self.user)
        self.assertEqual(
            response.context["title"], f"Корзина пользователя: {self.user.username}")

    def test_user_logout(self):
        self.client.login(username="tarantino", password="geekbrains")

        response = self.client.get("/auth/login/")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["user"].is_anonymous)

        response = self.client.get("/auth/logout/")
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["title"], "Главная")
        self.assertTrue(response.context["user"].is_anonymous)

    def test_user_register(self):
        response = self.client.get("/auth/register/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["title"], "регистрация")
        self.assertTrue(response.context["user"].is_anonymous)

        user_data = {
            "username": "samuel",
            "first_name": "Сэмюэл",
            "last_name": "Джексон",
            "password1": "geekbrains",
            "password2": "geekbrains",
            "email": "sumuel@geekshop.local",
            "age": "21",
        }

        response = self.client.post("/auth/register/", data=user_data)
        self.assertEqual(response.status_code, 200)

        user = ShopUser.objects.get(username=user_data["username"])

        activate = f"{settings.DOMAIN_NAME}/auth/verify/{user.id}/{user.auth_key}/"

        response = self.client.get(activate)
        self.assertEqual(response.status_code, 200)

        self.client.login(
            username=user_data["username"], password=user_data["password1"])

        response = self.client.get("/auth/login/")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["user"].is_anonymous)

        response = self.client.get("/")
        self.assertContains(
            response, text=user_data["username"], status_code=200)

    def test_user_wrong_register(self):
        # because of ajax realization, response of "register" controller is Json-object.
        # Thats why we need to convert json to python object brfore testing
        import json
        new_user_data = {
            "username": "teen",
            "first_name": "Мэри",
            "last_name": "Поппинс",
            "password1": "geekbrains",
            "password2": "geekbrains",
            "email": "merypoppins@geekshop.local",
            "age": "17",
        }
        response = self.client.post("/auth/register/", data=new_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['errors'])
        self.assertIn("Вы слишком молоды", json.loads(
            response.content)['form'])
