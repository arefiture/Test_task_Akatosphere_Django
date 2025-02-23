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
    amount = models.DecimalField(
        verbose_name='Количество',
        max_digits=6,
        decimal_places=2,
        validators=[
            MinValueValidator(
                limit_value=0.01,
                message='Количество должно быть не меньше 0.01.'
            ),
            MaxValueValidator(
                limit_value=9999.99,
                message='Количество не может превышать 9999.99.'
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
