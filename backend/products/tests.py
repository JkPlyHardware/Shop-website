from django.test import TestCase
from rest_framework.test import APIClient
from .models import Category, Product
class ProductAPITests(TestCase):
    def setUp(self):
        c = Category.objects.create(name="Tables")
        Product.objects.create(name="Sample Table", category=c, slug="sample-table")
    def test_product_list_returns_published_catalogue(self):
        response = APIClient().get("/api/products/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
