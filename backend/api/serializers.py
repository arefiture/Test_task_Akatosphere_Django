import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from products.models import Category, Product, ShoppingCart, Subcategory


class Base64ImageField(serializers.ImageField):
    """Сериалайзер под картинки. Преобразует входные данные в Base64."""

    def to_internal_value(self, data: str):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)

    def to_representation(self, value):
        """При чтении возвращает полный URL изображения."""
        if not value:
            return None

        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(value.url)

        return value.url


class CategorySerializer(serializers.ModelSerializer):
    """Заготовка под сериализаторы категорий."""
    image = Base64ImageField(label='Изображение')

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image']
        ref_name = 'Категория'


class SubcategorySerializer(CategorySerializer):
    """Сериалайзер подкатегорий (без категорий)."""

    class Meta(CategorySerializer.Meta):
        model = Subcategory
        ref_name = 'Подкатегория'


class CategoryWithSubcategorySerializer(CategorySerializer):
    """Сериалайзер категорий с подкатегориями."""
    subcategories = SubcategorySerializer(
        many=True, read_only=True
    )

    class Meta(CategorySerializer.Meta):
        model = Category
        fields = CategorySerializer.Meta.fields + ['subcategories']
        ref_name = 'Категории с подкатегориями'


class ProductImagesSerializer(serializers.Serializer):
    """Сериализатор для изображений в нужном формате."""
    image_big = Base64ImageField(label='Большое изображение')
    image_medium = Base64ImageField(label='Среднее изображение')
    image_small = Base64ImageField(label='Малое изображение')

    class Meta:
        ref_name = 'Изображения продуктов'


class ProductSerializer(serializers.ModelSerializer):
    """Сериалайзер продуктов."""
    category = serializers.SerializerMethodField(label='Категория')
    subcategory = SubcategorySerializer(read_only=True)
    images = ProductImagesSerializer(source='*', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'category', 'subcategory', 'price', 'images',
        ]
        ref_name = 'Продукт'

    def get_category(self, obj):
        """Получает родительскую категорию через подкатегорию."""
        request = self.context.get('request')
        if obj.subcategory and obj.subcategory.parent_category:
            return CategorySerializer(
                obj.subcategory.parent_category,
                context={'request': request}
            ).data
        return None  # На случай, если None будет разрешен... когда-нибудь


class ShoppingCartShortSerializer(serializers.ModelSerializer):
    """Продукты для взаимодействий с корзиной (фулл-очистка и суммы)."""
    product = ProductSerializer()

    class Meta:
        model = ShoppingCart
        fields = ['id', 'product', 'amount']
        read_only_fields = ['id']
        ref_name = 'Корзина (без автора)'


class ShoppingCartSerializer(ShoppingCartShortSerializer):
    """Сериализатор для корзины покупок."""
    product = ProductSerializer()

    class Meta(ShoppingCartShortSerializer.Meta):
        fields = ShoppingCartShortSerializer.Meta.fields + ['author']
        read_only_fields = ['id', 'author']
        ref_name = 'Корзина (с автором)'


class ShoppingCartListSerializer(serializers.Serializer):
    items = ShoppingCartShortSerializer(many=True)
    total_items = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ref_name = 'Список элементов корзины с суммами.'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['items'] = ShoppingCartShortSerializer(
            instance['items'], many=True
        ).data
        representation['total_items'] = instance['total_items']
        representation['total_price'] = instance['total_price']
        return representation
