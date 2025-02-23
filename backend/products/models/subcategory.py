from django.db import models

from products.models.abstract_models import AbstractCategoryModel
from products.models.category import Category


class Subcategory(AbstractCategoryModel):
    """Модель подкатегорий."""
    parent_category = models.ForeignKey(
        to=Category,
        verbose_name='Родительская категория',
        on_delete=models.CASCADE,
        related_name='subcategories'
    )

    class Meta:
        verbose_name = 'подкатегорию'
        verbose_name_plural = 'Подкатегории'
        ordering = AbstractCategoryModel.Meta.ordering
