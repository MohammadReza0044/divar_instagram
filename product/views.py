from rest_framework import generics, status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Product, ProductComment, ProductFavorite, ProductLike
from .serializers import (
    ProductCommentSerializer,
    ProductFavoriteSerializer,
    ProductLikeSerializer,
    ProductSerializer,
)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductCommentViewSet(ListCreateAPIView):
    queryset = ProductComment.objects.all()
    serializer_class = ProductCommentSerializer

    def list(self, request, product_id=None):
        queryset = ProductComment.objects.filter(product=product_id)
        serializer = ProductCommentSerializer(queryset, many=True)
        return Response(serializer.data)


class ProductLikeCreate(ListCreateAPIView):
    queryset = ProductLike.objects.all()
    serializer_class = ProductLikeSerializer
    # permission_classes = [IsAuthenticated]

    def list(self, request):
        user = self.request.user
        queryset = ProductLike.objects.filter(user=user.pk)
        serializer = ProductLikeSerializer(queryset, many=True)
        return Response(serializer.data)


class ProductLikeProductList(generics.ListAPIView):
    serializer_class = ProductLikeSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_id = self.kwargs["product_id"]
        queryset = ProductLike.objects.filter(product_id=product_id)
        serializer = ProductLikeSerializer(queryset, many=True)
        return queryset


class ProductLikeDeleteView(generics.RetrieveDestroyAPIView):
    queryset = ProductLike.objects.all()
    serializer_class = ProductLikeSerializer
    lookup_field = "pk"
    # permission_classes = [IsAuthenticated]


class ProductFavoriteViewSet(ModelViewSet):
    serializer_class = ProductFavoriteSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ProductFavorite.objects.filter(user=user.pk)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if the object already exists
        user = serializer.validated_data.get("user")
        product = serializer.validated_data.get("product")
        if ProductFavorite.objects.filter(product=product, user=user).exists():
            return Response(
                {"detail": "Object already exists."}, status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
