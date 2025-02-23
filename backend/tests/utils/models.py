from django.db.models import Model


def category_model() -> Model:
    from products.models.category import Category
    return Category


def subcategory_model() -> Model:
    from products.models.subcategory import Subcategory
    return Subcategory
