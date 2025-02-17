from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from products.models.product import Product

User = get_user_model()


class ShoppingCart(models.Model):
    """Модель корзины покупок."""
    author = models.ForeignKey(
        to=User,
        verbose_name='Автор корзины',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        to=Product,
        verbose_name='Продукт',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Количество должно быть равно 1 или больше.'
            ),
            MaxValueValidator(
                limit_value=9999,
                message='Количество не может превышать 9999'
            )
        ]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'product'),
                name='unique_shopping_cart'
            )
        ]
        default_related_name = 'shopping_cart'
        verbose_name = 'Продукт в корзине'
        verbose_name_plural = 'Продукты в корзине'
