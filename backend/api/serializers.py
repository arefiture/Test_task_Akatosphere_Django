import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from products.models import Category, Product, Subcategory


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
    image = Base64ImageField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image']


class SubcategorySerializer(CategorySerializer):
    """Сериалайзер подкатегорий (без категорий)."""

    class Meta(CategorySerializer.Meta):
        model = Subcategory


class CategoryWithSubcategorySerializer(CategorySerializer):
    """Сериалайзер категорий с подкатегориями."""
    subcategories = SubcategorySerializer(
        many=True, read_only=True
    )

    class Meta(CategorySerializer.Meta):
        model = Category
        fields = CategorySerializer.Meta.fields + ['subcategories']


class ProductImagesSerializer(serializers.Serializer):
    """Сериализатор для изображений в нужном формате."""
    image_big = Base64ImageField()
    image_medium = Base64ImageField()
    image_small = Base64ImageField()


class ProductSerializer(serializers.ModelSerializer):
    """Сериалайзер продуктов."""
    category = serializers.SerializerMethodField()
    subcategory = SubcategorySerializer(read_only=True)
    images = ProductImagesSerializer(source='*', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'category', 'subcategory', 'price', 'images',
        ]

    def get_category(self, obj):
        """Получает родительскую категорию через подкатегорию."""
        request = self.context.get('request')
        if obj.subcategory and obj.subcategory.parent_category:
            return CategorySerializer(
                obj.subcategory.parent_category,
                context={'request': request}
            ).data
        return None  # На случай, если None будет разрешен... когда-нибудь
