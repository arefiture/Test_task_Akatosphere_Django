import pytest
from pytest_lazyfixture import lazy_fixture
from rest_framework.test import APIClient

from tests.base_test import BaseTest
from tests.utils.category import (
    RESPONSE_SCHEMA_CATEGORY_WITH_SUB,
    URL_CATEGORY,
)


@pytest.mark.django_db(transaction=True)
class TestCategories(BaseTest):

    @pytest.mark.parametrize(
        'client',
        [
            lazy_fixture('api_client'),
            lazy_fixture('first_user_authorized_client')
        ]
    )
    @pytest.mark.usefixtures('subcategories')
    def test_get_categories_with_sub(self, client: APIClient):
        self.url_get_resource(
            client=client,
            url=URL_CATEGORY,
            response_schema=RESPONSE_SCHEMA_CATEGORY_WITH_SUB
        )
