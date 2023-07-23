import io

from django.urls import reverse
from PIL import Image
from rest_framework.test import APITestCase

from user.models import User

from .models import Product, ProductComment


class ProductViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(first_name="testuser")
        self.object = Product.objects.create(
            add_title="Test Object 1", price=1000, user=self.user
        )

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new("RGBA", size=(100, 100), color=(155, 0, 0))
        image.save(file, "png")
        file.name = "test.png"
        file.seek(0)
        return file

    def test_list_object(self):
        url = reverse("product:product-list")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_object(self):
        photo_file = self.generate_photo_file()
        url = reverse("product:product-list")
        data = {
            "user": self.user.pk,
            "add_title": "Test Object 2",
            "category": "موبایل",
            "city": "Test Object",
            "Neighbourhood": "Test Object",
            "brand_name": "Test Object",
            "device_model": "Test Object",
            "device_status": "در حد نو",
            "brand_originality": "اصل",
            "price": 1000,
            "description": "Test Object",
            "uploaded_images": photo_file,
        }

        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 2)

    def test_patch_object(self):
        photo_file = self.generate_photo_file()
        url = reverse("product:product-detail", args=[self.object.pk])
        data = {
            "price": 2000,
            "update_photos": photo_file,
        }

        response = self.client.patch(url, data, format="multipart")
        self.assertEqual(response.status_code, 200)

    def test_delete_photo(self):
        url = reverse("product:product-detail", args=[self.object.pk])
        data = {
            "delete_photos": 1,
        }

        response = self.client.patch(url, data, format="multipart")
        self.assertEqual(response.status_code, 200)

    def test_delete_object(self):
        url = reverse("product:product-detail", args=[self.object.pk])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)


class ProductCommentViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(first_name="testuser")
        self.product = Product.objects.create(
            add_title="Test Object 1", price=1000, user=self.user
        )

    def test_list_comment(self):
        url = reverse("product:product-comment-list", args=[self.product.pk])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_comment(self):
        url = reverse("product:product-comment-list")
        data = {
            "user": self.user.pk,
            "product": self.product.pk,
            "text": "Test Body for this comment",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ProductComment.objects.count(), 1)
        self.assertEqual(
            ProductComment.objects.get().text, "Test Body for this comment"
        )
