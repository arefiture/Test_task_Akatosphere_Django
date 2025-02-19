from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView

from api.pagination import CategoryPagination, ProductPagination
from api.serializers import (
    CategoryWithSubcategorySerializer,
    ProductSerializer
)
from products.models import Category, Product


class CategoryListView(ListAPIView):
    """Вьюшка просмотра списка всех категорий с вложенными подкатегориями."""
    queryset = Category.objects.all()
    serializer_class = CategoryWithSubcategorySerializer
    permission_classes = [AllowAny]
    pagination_class = CategoryPagination


class ProductListView(ListAPIView):
    """Вьюшка просмотра списка всех продуктов."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    pagination_class = ProductPagination
