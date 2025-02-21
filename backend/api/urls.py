from django.urls import path, include

from api.views import (
    CategoryListView,
    ProductListView,
    ProductShopActionView,
    ShoppingCartView
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
]
