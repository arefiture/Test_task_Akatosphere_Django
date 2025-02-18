import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from products.models import Category, Subcategory


class Base64ImageField(serializers.ImageField):
    """Сериалайзер под картинки. Преобразует входные данные в Base64."""

    def to_internal_value(self, data: str):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class AbstractCategorySerializer(serializers.ModelSerializer):
    """Заготовка под сериализаторы категорий."""
    image = Base64ImageField()

    class Meta:
        fields = ['id', 'name', 'slug', 'image']


class SubcategorySerializer(AbstractCategorySerializer):

    class Meta(AbstractCategorySerializer.Meta):
        model = Subcategory


class CategoryWithSubcategorySerializer(AbstractCategorySerializer):
    subcategories = SubcategorySerializer(
        many=True, read_only=True
    )

    class Meta(AbstractCategorySerializer.Meta):
        model = Category
        fields = AbstractCategorySerializer.Meta.fields + ['subcategories']
