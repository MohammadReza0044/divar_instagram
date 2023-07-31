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
    path(
        "product-like-create/",
        views.ProductLikeCreate.as_view(),
        name="product-like-create",
    ),
    path(
        "product-like-user-list/",
        views.ProductLikeCreate.as_view(),
        name="product-like-user-list",
    ),
    path(
        "product-like-product-list/<int:product_id>/",
        views.ProductLikeProductList.as_view(),
        name="product-like-product-list",
    ),
    path(
        "product-like-delete/<int:pk>/",
        views.ProductLikeDeleteView.as_view(),
        name="product-like-delete",
    ),
]
