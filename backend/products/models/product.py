from django.db import models

from products.models.abstract_models import AbstractNameSlugModel
from products.models.subcategory import Subcategory


class Product(AbstractNameSlugModel):
    """Модель продуктов."""
    subcategory = models.ForeignKey(
        to=Subcategory,
        verbose_name='Подкатегория',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=8,
        decimal_places=2,
    )
    image_big = models.ImageField(
        verbose_name='Путь до большой картинки',
        blank=True,
        upload_to='products/image/big/'
    )
    image_medium = models.ImageField(
        verbose_name='Путь до средней картинки',
        blank=True,
        upload_to='products/image/medium/'
    )
    image_small = models.ImageField(
        verbose_name='Путь до маленькой картинки',
        blank=True,
        upload_to='products/image/small'
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = AbstractNameSlugModel.Meta.ordering
