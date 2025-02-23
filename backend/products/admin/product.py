from django.contrib import admin
from django.forms.models import ModelChoiceField

from products.admin.abstract import AbstractNameSlugAdmin
from products.models import Product, Subcategory


class SubcategoryChoiceField(ModelChoiceField):
    """Кастомное поле для отображения подкатегорий с родительской категорией"""

    def label_from_instance(self, obj):
        return f"{obj.parent_category.name} - {obj.name}"


@admin.register(Product)
class ProductAdmin(AbstractNameSlugAdmin):
    """Страничка управления категориями в админке."""

    list_display = AbstractNameSlugAdmin.list_display + [
        'subcategory', 'get_category', 'price', 'image_big', 'image_medium',
        'image_small',
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subcategory":
            kwargs['form_class'] = SubcategoryChoiceField
            kwargs['queryset'] = Subcategory.objects.select_related(
                'parent_category'
            ).all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_category(self, obj):
        return obj.subcategory.parent_category.name
    get_category.short_description = 'Категория'
