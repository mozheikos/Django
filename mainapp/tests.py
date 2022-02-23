from django.test import TestCase
from django.core.management import call_command
from django.test.client import Client

from authnapp.models import ShopUser
from mainapp.models import Product, Category


class TestMainappSmoke(TestCase):
    fixtures = [
        "mainapp/fixtures/001_category.json",
        "mainapp/fixtures/002_products.json",
        "mainapp/fixtures/003_contacts.json",
        "authnapp/fixtures/admin.json",
    ]

    def setUp(self) -> None:
        self.client = Client()

    def test_fixtures_load(self):
        self.assertGreater(Category.objects.count(), 0)
        self.assertGreater(Product.objects.count(), 0)

    def test_mainapp_urls(self):
        responce = self.client.get("/")
        self.assertEqual(responce.status_code, 200)

        responce = self.client.get("/contact/")
        self.assertEqual(responce.status_code, 200)

        responce = self.client.get("/products/")
        self.assertEqual(responce.status_code, 200)

        for category in Category.objects.all():
            responce = self.client.get(f"/products/{category.pk}/page/1/")
            self.assertEqual(responce.status_code, 200)

        for product in Product.objects.all():
            responce = self.client.get(
                f"/products/{product.category_id}/{product.id}/")
            self.assertEqual(responce.status_code, 200)


class ProductsTestCase(TestCase):
    def test_product_print(self):
        product_1 = Product.objects.get(name="комфорт 1")
        product_2 = Product.objects.get(name="комфорт 2")
        self.assertEqual(str(product_1), "комфорт 1 - (дом)")
        self.assertEqual(str(product_2), "комфорт 2 - (дом)")

    def test_product_get_items(self):
        product_1 = Product.objects.get(name="комфорт 1")
        product_3 = Product.objects.get(name="комфорт 2")

        products_as_class_method = set(product_1.get_items())
        products = set([product_1, product_3])

        self.assertIsNotNone(products_as_class_method.intersection(products))

    def test_category_products(self):
        length = Category.objects.count()
        for i in range(2, length):
            category = Category.objects.get(pk=i)
            self.assertIsNotNone(category.category_products)
