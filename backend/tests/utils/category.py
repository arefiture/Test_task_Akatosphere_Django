# Адреса страниц

URL_CATEGORY = '/api/category/'

# Структуры для перебора

CATEGORY_DATA = [
    {
        'name': 'Продукты питания',
        'slug': 'food',
        'image': 'category/image/food.png'
    },
    {
        'name': 'Бытовая химия и гигиена',
        'slug': 'household-chemistry-hygiene',
        'image': 'category/image/household-chemistry-hygiene.png'
    }
]

SUBCATEGORY_DATA = [  # parent_category_id в фикстурах в любом случае будет -1
    {
        'name': 'Фрукты и овощи',
        'slug': 'fruits-vegetables',
        'image': 'category/image/fruits-vegetables.png',
        'parent_category_id': 1
    },
    {
        'name': 'Молочные продукты',
        'slug': 'dairy',
        'image': 'category/image/dairy.png',
        'parent_category_id': 1
    },
    {
        'name': 'Средства для уборки',
        'slug': 'cleaning-products',
        'image': 'category/image/cleaning-products.png',
        'parent_category_id': 2
    },
]

RESPONSE_SCHEMA_CATEGORY = {
    'type': 'object',
    'properties': {
        'id': {'type': 'number'},
        'name': {'type': 'string'},
        'slug': {'type': 'string'},
        'image': {'type': 'string'},
        'subcategories': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'number'},
                    'name': {'type': 'string'},
                    'slug': {'type': 'string'},
                    'image': {'type': 'string'}
                },
                'required': ['id', 'name', 'slug', 'image'],
                'additionalProperties': False
            }
        }
    }
}

RESPONSE_SCHEMA_CATEGORY_WITH_SUB = {
    'type': 'object',
    'required': ['count', 'next', 'previous', 'results'],
    'additionalProperties': False,
    'properties': {
        'count': {'type': 'number'},
        'next': {'type': ['string', 'null']},
        'previous': {'type': ['string', 'null']},
        'results': {
            'type': 'array',
            'items': RESPONSE_SCHEMA_CATEGORY
        }
    }
}
