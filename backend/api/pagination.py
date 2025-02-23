from rest_framework.pagination import PageNumberPagination


class BasePagination(PageNumberPagination):
    """Базовый класс пагинации."""
    page_size = 10
    page_query_param = 'page_size'  # Размер страницы


class CategoryPagination(BasePagination):
    max_page_size = 100  # Максимальное количество категорий на странице


class ProductPagination(BasePagination):
    max_page_size = 50
