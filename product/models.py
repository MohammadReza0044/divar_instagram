from django.db import models

from user.models import User


class Product(models.Model):
    CATEGORY_TYPE_CHOICES = (
        ("موبایل", "موبایل"),
        ("تبلت", "تبلت"),
    )
    DEVICE_STATUS_TYPE_CHOICES = (
        ("در حد نو", "در حد نو"),
        ("کار کرده", "کار کرده"),
        ("نیاز به تعمیر", "نیاز به تعمیر"),
    )
    ORIGINALITY_TYPE_CHOICES = (
        ("اصل", "اصل"),
        ("غیر اصل", "غیر اصل"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    add_title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_TYPE_CHOICES)
    city = models.CharField(max_length=100)
    Neighbourhood = models.CharField(max_length=100)
    brand_name = models.CharField(max_length=100)
    device_model = models.CharField(max_length=100)
    device_status = models.CharField(max_length=50, choices=DEVICE_STATUS_TYPE_CHOICES)
    brand_originality = models.CharField(
        max_length=50, choices=ORIGINALITY_TYPE_CHOICES
    )
    price = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = "Product"

    def __str__(self):
        return self.add_title


class ProductPhoto(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="Product/images", null=True)

    class Meta:
        db_table = "Product Photos"


class ProductComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    status = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Product Comment"
        ordering = ["-created_at"]

    def __str__(self):
        return self.text
