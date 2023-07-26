from rest_framework import serializers

from .models import Product, ProductComment, ProductLike, ProductPhoto


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = ["id", "image"]


class ProductSerializer(serializers.ModelSerializer):
    images = PhotoSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(
            max_length=1000000, allow_empty_file=False, use_url=False
        ),
        write_only=True,
    )
    delete_photos = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )
    update_photos = serializers.ListField(
        child=serializers.ImageField(), required=False
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "user",
            "add_title",
            "category",
            "city",
            "Neighbourhood",
            "brand_name",
            "device_model",
            "device_status",
            "brand_originality",
            "price",
            "description",
            "uploaded_images",
            "delete_photos",
            "update_photos",
            "images",
        ]

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        product = Product.objects.create(**validated_data)
        for image in uploaded_images:
            newproduct_image = ProductPhoto.objects.create(product=product, image=image)
        return product

    def update(self, instance, validated_data):
        delete_photos = validated_data.pop("delete_photos", None)
        update_photos = validated_data.pop("update_photos", None)

        # Delete photos
        if delete_photos:
            ProductPhoto.objects.filter(id__in=delete_photos, product=instance).delete()

        # Update photos
        if update_photos:
            for image in update_photos:
                newproduct_image = ProductPhoto.objects.create(
                    product=instance, image=image
                )

        return super().update(instance, validated_data)


class ProductCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = ["id", "user", "product", "text"]


class ProductLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLike
        fields = "__all__"
