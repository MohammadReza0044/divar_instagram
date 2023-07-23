from django.urls import include, path
from rest_framework import routers

from product import views

app_name = "product"

router = routers.SimpleRouter()
router.register("product", views.ProductViewSet, basename="product")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "product-comment/<int:product_id>/",
        views.ProductCommentViewSet.as_view(),
        name="product-comment-list",
    ),
    path(
        "product-comment/create/",
        views.ProductCommentViewSet.as_view(),
        name="product-comment-create",
    ),
]
