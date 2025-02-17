from django.contrib import admin

from products.admin.abstract import AbstractCategoryAdmin
from products.models import Category


@admin.register(Category)
class CategoryAdmin(AbstractCategoryAdmin):
    """Страничка управления категориями в админке."""

    pass
