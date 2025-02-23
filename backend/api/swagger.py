from drf_yasg import openapi
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED
)

from api.serializers import ShoppingCartListSerializer, ShoppingCartSerializer


# Переменные / Поля

PAGE_SIZE_SCHEMA = dict(
    name='page_size',  # Имя параметра
    in_=openapi.IN_QUERY,  # Где находится (query/path/body)
    description="Количество элементов на странице",
    type=openapi.TYPE_INTEGER,
    default=10,
)

# Сами схемы под эндпоинты

CATEGORY_PARAM_SCHEMA = dict(
    manual_parameters=[
        openapi.Parameter(
            **PAGE_SIZE_SCHEMA,
            maximum=100
        )
    ]
)

PRODUCT_PARAM_SCHEMA = dict(
    manual_parameters=[
        openapi.Parameter(
            **PAGE_SIZE_SCHEMA,
            maximum=50
        )
    ]
)

SHOP_ACTION_PARAM_SCHEMA = dict(
    manual_parameters=[
        openapi.Parameter(
            name='id',  # Имя параметра
            in_=openapi.IN_PATH,  # Где находится (query/path/body)
            description='Идентификатор продукта',
            type=openapi.TYPE_INTEGER,
        )
    ]
)

SHOP_ACTION_POST_RESPONSES_SCHEMA = dict(
    responses={
            HTTP_200_OK: openapi.Response(
                description='Количество обновлено',
                schema=ShoppingCartSerializer()
            ),
            HTTP_201_CREATED: openapi.Response(
                description='Продукт(ы) добавлен(ы) в корзину',
                schema=ShoppingCartSerializer()
            ),
        }
)

SHOP_CART_RESPONSES_SCHEMA = dict(
    responses={
            HTTP_200_OK: openapi.Response(
                description='Количество обновлено',
                schema=ShoppingCartSerializer()
            ),
        }
)

SHOP_CART_LIST_RESPONSES_SCHEMA = dict(
    responses={
            HTTP_200_OK: openapi.Response(
                description='Состав корзины вернулся успешно',
                schema=ShoppingCartListSerializer()
            ),
        }
)
