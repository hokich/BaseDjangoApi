from rest_framework import viewsets

from utils.response_service import ResponseService

from . import services
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = services.get_all_products()
    serializer_class = ProductSerializer
    allowed_methods = ["GET", "POST", "PUT", "DELETE"]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return ResponseService.success(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ResponseService.success(data=serializer.data)
