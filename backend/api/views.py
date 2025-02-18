from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView

from api.pagination import CategoryPagination
from api.serializers import CategoryWithSubcategorySerializer
from products.models import Category


class CategoryListView(ListAPIView):
    """Вьюшка просмотра списка всех категорий с вложенными подкатегориями."""
    queryset = Category.objects.all()
    serializer_class = CategoryWithSubcategorySerializer
    permission_classes = [AllowAny]
    pagination_class = CategoryPagination
