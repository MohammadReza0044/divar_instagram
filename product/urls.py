from django.urls import include, path
from rest_framework import routers

from product import views

app_name = "product"

router = routers.SimpleRouter()
router.register("product", views.ProductViewSet, basename="product")
router.register(
    "product-comment",
    views.ProductCommentViewSet,
    basename="product-comment",
)


urlpatterns = [
    path("", include(router.urls)),
    path(
        "product-comment/<int:product_id>",
        views.ProductCommentViewSet.as_view({"get": "list"}),
        name="product-comment-list",
    ),
]
