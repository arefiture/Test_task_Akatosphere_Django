from django.contrib import admin

from products.admin.abstract import AbstractCategoryAdmin
from products.models import Subcategory


@admin.register(Subcategory)
class SubcategoryAdmin(AbstractCategoryAdmin):
    """Страничка управления категориями в админке."""

    list_display = AbstractCategoryAdmin.list_display + ['parent_category']
    list_filter = ['parent_category']
