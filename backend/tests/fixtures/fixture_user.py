import pytest
from django.contrib.auth import get_user_model
from django.db.models import Model
from rest_framework.test import APIClient

from tests.utils.user import (
    FIRST_USER,
    SECOND_USER,
    THIRD_USER,
    URL_LOGIN
)

User = get_user_model()


def create_user(django_user_model, user_data) -> Model:
    return django_user_model.objects.create_user(
        **user_data
    )


def get_user_token(user: str, password: str) -> dict[str, str]:
    client = APIClient()
    response = client.post(URL_LOGIN, {
        'username': user.username,
        'password': password
    })
    return {
        'access': response.data.get('access'),
        'refresh': response.data.get('refresh')
    }


def authorized_client(token: str) -> APIClient:
    client = APIClient()
    access_token = token['access']
    client.credentials(
        HTTP_AUTHORIZATION=f'Bearer {access_token}'
    )
    return client


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def first_user(django_user_model: Model) -> Model:
    return create_user(django_user_model, FIRST_USER)


@pytest.fixture
def second_user(django_user_model: Model) -> Model:
    return create_user(django_user_model, SECOND_USER)


@pytest.fixture
def third_user(django_user_model: Model) -> Model:
    return create_user(django_user_model, THIRD_USER)


@pytest.fixture
def all_user(first_user: Model, second_user: Model, third_user: Model) -> list:
    return [first_user, second_user, third_user]


@pytest.fixture
def first_user_token(first_user: Model) -> dict:
    return get_user_token(
        user=first_user, password=FIRST_USER['password']
    )


@pytest.fixture
def second_user_token(second_user: Model) -> dict:
    return get_user_token(
        user=second_user, password=SECOND_USER['password']
    )


@pytest.fixture
def third_user_token(third_user: Model) -> dict:
    return get_user_token(
        user=third_user, password=THIRD_USER['password']
    )


@pytest.fixture
def first_user_authorized_client(first_user_token: dict) -> APIClient:
    return authorized_client(token=first_user_token)


@pytest.fixture
def second_user_authorized_client(second_user_token: dict) -> APIClient:
    return authorized_client(token=second_user_token)


@pytest.fixture
def third_user_authorized_client(third_user_token: dict) -> APIClient:
    return authorized_client(token=third_user_token)
