import pytest

from tests.utils.models import category_model, subcategory_model
from tests.utils.category import CATEGORY_DATA, SUBCATEGORY_DATA

Category = category_model()
Subcategory = subcategory_model()


@pytest.fixture
def categories():
    categories = [Category(**item) for item in CATEGORY_DATA]
    Category.objects.bulk_create(categories)
    return list(Category.objects.all())


@pytest.fixture
def subcategories(categories):
    subcategories = [
        Subcategory(**{
            'name': item['name'],
            'slug': item['slug'],
            'image': item['image'],
            'parent_category': categories[item['parent_category_id'] - 1]
        }) for item in SUBCATEGORY_DATA
    ]
    Subcategory.objects.bulk_create(subcategories)
    return list(Subcategory.objects.all())
