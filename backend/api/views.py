from django.db.models import Sum, F
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    # HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.views import APIView

from api.pagination import CategoryPagination, ProductPagination
from api.serializers import (
    CategoryWithSubcategorySerializer,
    ProductSerializer,
    ShoppingCartSerializer,
    ShoppingCartShortSerializer
)
from products.models import (
    Category,
    Product,
    ShoppingCart
)


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


class ProductShopActionView(APIView):
    """Вьюшка для добавления продукта в корзину."""

    # Не вижу смысла в patch методе в этом варианте реализации.
    def post(self, request, id):
        """Добавление/обновление продукта в корзине."""
        product = get_object_or_404(Product, id=id)
        amount = request.data.get('amount', 1)

        amount = self.validate_amount(amount)

        cart_item, created = ShoppingCart.objects.update_or_create(
            author=request.user,
            product=product,
            defaults={'amount': amount}
        )
        serializer = ShoppingCartSerializer(cart_item)
        return Response(
            serializer.data,
            status=HTTP_201_CREATED if created else HTTP_200_OK
        )

    def delete(self, request, id):
        """Удаление продукта из корзины."""
        cart_item = get_object_or_404(
            ShoppingCart, author=request.user,
            product_id=id
        )
        cart_item.delete()
        return Response(
            {'message': 'Продукт удален из корзины.'},
            status=HTTP_200_OK  # Лучше HTTP_204_NO_CONTENT
            # Но в постмане от этого падают тесты =(
        )

    @staticmethod
    def validate_amount(amount):
        """Проверка количества."""
        try:
            amount = int(amount)
            if amount < 1 or amount > 9999:
                raise ValidationError('Количество должно быть от 1 до 9999.')
            return amount
        except (ValueError, TypeError):
            raise ValidationError('Некорректное значение количества.')


class ShoppingCartView(APIView):
    """Вюшка для просмотра и очистки корзины."""

    def get(self, request):
        """Возвращает состав корзины с общей стоимостью и количеством."""
        cart_items = ShoppingCart.objects.filter(
            author=request.user
        ).select_related('product')

        # TODO вынести агрегатки в total_value()
        total_items = cart_items.aggregate(
            total_count=Sum('amount')
        )['total_count'] or 0
        total_price = cart_items.aggregate(
            total_price=Sum(F('amount') * F('product__price'))
        )['total_price'] or 0

        return Response({
            'items': ShoppingCartShortSerializer(cart_items, many=True).data,
            'total_items': total_items,
            'total_price': total_price
        }, status=HTTP_200_OK)

    def delete(self, request):
        """Очищает корзину пользователя."""
        cart_items = ShoppingCart.objects.filter(author=request.user)

        if cart_items.exists():
            cart_items.delete()
            # Обычно "нет контента", но я посчитал 200 в этом случае лучшим
            return Response(
                {'message': 'Корзина очищена.'},
                status=HTTP_200_OK
            )
        else:
            # BAD-т.к. нельзя удалить то, чего нет.
            return Response(
                {'message': 'Корзина пуста.'},
                status=HTTP_400_BAD_REQUEST
            )
