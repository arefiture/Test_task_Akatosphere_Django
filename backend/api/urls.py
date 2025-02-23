from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.urls import path, include
from rest_framework.permissions import AllowAny  # TODO: заменить IsAdminUser

from api.views import (
    CategoryListView,
    ProductListView,
    ProductShopActionView,
    ShoppingCartView
)

schema_view = get_schema_view(
    openapi.Info(
        title="API проекта TestTaskAkatosphereDjango",
        default_version='v1',
        description="Описаны ключевые эндпоинты (кроме /admin/).",
    ),
    public=True,
    permission_classes=(AllowAny,),
)


urlpatterns = [
    path('auth/', include('api.auth.urls')),
    path('category/', CategoryListView.as_view(), name='category'),
    path('product/', ProductListView.as_view(), name='product'),
    path(
        'product/<int:id>/shop_action/', ProductShopActionView.as_view(),
        name='product-shop-action'
    ),
    path('shopping_cart/', ShoppingCartView.as_view(), name='shopping_cart'),
    path(
        'swagger/', schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path(
        'redoc/', schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
]
