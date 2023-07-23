from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Product, ProductComment
from .serializers import ProductCommentSerializer, ProductSerializer


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
