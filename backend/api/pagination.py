from django.conf import settings

from rest_framework.pagination import PageNumberPagination


class BasePagination(PageNumberPagination):
    """Базовый класс пагинации."""
    page_size = settings.PAGINATION.get('DEFAULT_PAGE_SIZE', 10)
    # Размер страницы:
    page_query_param = settings.PAGINATION.get('PAGE_QUERY_PARAM', 'page_size')


class CategoryPagination(BasePagination):
    max_page_size = page_size = settings.PAGINATION.get(
        'CATEGORY_MAX_PAGE_SIZE', 100
    )


class ProductPagination(BasePagination):
    max_page_size = page_size = settings.PAGINATION.get(
        'PRODUCT_MAX_PAGE_SIZE', 50
    )
