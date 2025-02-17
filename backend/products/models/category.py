from products.models.abstract_models import AbstractCategoryModel


class Category(AbstractCategoryModel):
    """Модель категорий."""

    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = 'Категории'
        ordering = AbstractCategoryModel.Meta.ordering
