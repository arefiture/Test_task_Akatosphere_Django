from http import HTTPStatus
from typing import Any, Optional, Union

from django.db.models import Model
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.test import APIClient

from tests.utils.general import (
    RESPONSE_EXPECTED_STRUCTURE,
    URL_BAD_REQUEST_ERROR,
    URL_CREATED_ERROR,
    URL_FORBIDDEN_ERROR,
    URL_FOUND_ERROR,
    URL_METHOD_NOT_ALLOWED,
    URL_NO_CONTENT_ERROR,
    URL_NOT_FOUND_ERROR,
    URL_OK_ERROR,
    URL_UNAUTHORIZED_ERROR
)


class BaseTest:

    def _url_is_accessible(
        self, response: Response, url: str
    ):
        """
        Функция (внутренняя) для проверки доступности url.

        Принимает:
        * response - Ответ на запрос к url
        * url - Адрес запроса

        Assert в случаях:
        * Если страница не найдена
        """
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            URL_NOT_FOUND_ERROR.format(url=url)
        )

    def _response_matches_schema(
        self, data: Union[dict, list], response_schema: dict[str, Any]
    ):
        """
        Функция (внутренняя) для проверки схемы ответа.

        Принимает:
        * data - Ответ на запрос к url в виде словаря
        * response_schema - Ожидаемая схема ответа

        Assert в случаях:
        * Если структура не соответствует ожидаемой
        """
        try:
            validate(
                instance=data,
                schema=response_schema
            )
        except ValidationError:
            assert False, RESPONSE_EXPECTED_STRUCTURE

    def url_is_missing_for_method(
        self, client: APIClient, url: str, method: str
    ):
        """
        Функция для проверки недоступности url.

        Принимает:
        * client - Клиент для запроса
        * url - Адрес запроса
        * method - Метод, используемый при отправке запроса

        Assert в случаях:
        * Если страница доступна
        """
        response: Response = getattr(client, method)(url)
        assert response.status_code == HTTPStatus.NOT_FOUND, (
            URL_NOT_FOUND_ERROR.format(url=url)
        )

    def url_requires_authorization(
        self, client: APIClient, url: str, method: str = 'post',
        data: Optional[dict[str, Any]] = None
    ):
        """
        Функция на проверку недоступности урла анониму.

        Принимает:
        * client - Клиент для запроса. Ожидается без авторизации
        * url - Адрес запроса
        * method - Метод, используемый при отправке запроса. По умолчанию post
        * data - Опционально. Ответ на запрос к url в виде словаря

        Assert в случаях:
        * Если страница не найдена
        * Если страница доступна анониму
        """
        response: Response = getattr(client, method)(url, data)
        self._url_is_accessible(response=response, url=url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            URL_UNAUTHORIZED_ERROR.format(url=url)
        )

    def url_bad_request_for_invalid_data(
        self, client: APIClient, url: str, method: str = 'post',
        data: Optional[dict[str, Any]] = None
    ):
        """
        Функция для проверки корректности запроса.

        Принимает:
        * client - Клиент для запроса. Ожидается без авторизации
        * url - Адрес запроса
        * method - Метод, используемый при отправке запроса. По умолчанию post
        * data - Опционально. Ответ на запрос к url в виде словаря

        Assert в случаях:
        * Если страница не найдена
        * Если в ответе код статуса 400.
        """
        response: Response = getattr(client, method)(url, data)
        self._url_is_accessible(response=response, url=url)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            URL_BAD_REQUEST_ERROR.format(url=url)
        )

    def url_creates_resource(
        self, *, client: APIClient, url: str, model: Model,
        filters: dict[str, Any], data: Optional[dict[str, Any]] = None,
        response_schema: dict[str, Any]
    ) -> Response:
        """
        Функция для проверки недоступности url.

        Принимает:
        * client - Клиент для запроса
        * url - Адрес запроса
        * data - Опционально. Ответ на запрос к url в виде словаря
        * model - Модель для проверки сохранения данных в БД
        * filters - Словарь данных, которые будут проверяться в БД
        * response_schema - Ожидаемая схема ответа

        Assert в случаях:
        * Если страница не найдена
        * Если страница не вернула статус 201 (успешное создание)
        * Если в БД не обновилась запись
        * Если структура не соответствует ожидаемой

        Возвращает:
        * reponse - Проверенный ответ
        """
        count_in_db = model.objects.count()
        response: Response = client.post(url, data=data)
        self._url_is_accessible(response=response, url=url)
        assert response.status_code == HTTPStatus.CREATED, (
            URL_CREATED_ERROR.format(url=url)
        )

        new_item_in_db = model.objects.filter(**filters)
        assert (
            new_item_in_db.exists()
            and count_in_db + 1 == new_item_in_db.count()
        ), 'Убедитесь, что в БД обновились записи.'

        self._response_matches_schema(
            data=response.json(),
            response_schema=response_schema
        )

        return response

    def url_get_resource(
        self, *, client: Optional[APIClient] = None, url: str,
        response_schema: dict[str, Any], response: Optional[Response] = None
    ):
        """
        Функция для проверки доступности GET-метода.

        Принимает:
        * client - Клиент для запроса. (Если не передан response)
        * response - Ответ на запрос к url. (Если не передан client)
        * url - Адрес запроса
        * response_schema - Ожидаемая схема ответа

        Assert в случаях:
        * Если страница не найдена
        * Если страница не вернула статус 200
        * Если структура не соответствует ожидаемой
        """
        if (client and response) or (not client and not response):
            raise ValueError('Нужно передавать либо client, либо response!')
        if client:
            response: Response = client.get(url)
        self._url_is_accessible(response=response, url=url)
        assert response.status_code == HTTPStatus.OK, (
            URL_OK_ERROR.format(url=url)
        )

        self._response_matches_schema(
            data=response.json(),
            response_schema=response_schema
        )

    def url_is_not_allowed_for_method(
        self, client: APIClient, url: str, method: str
    ):
        """
        Функция для проверки недоступности метода.

        Принимает:
        * client - Клиент для запроса
        * url - Адрес запроса
        * method - Метод, используемый при отправке запроса

        Assert в случаях:
        * Если страница не вернула статус 405 (метод не разрешен)
        """
        response: Response = getattr(client, method)(url)
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED, (
            URL_METHOD_NOT_ALLOWED.format(method=method.upper(), url=url)
        )

    def url_put_success_status(
        self, client: APIClient, url: str, model: Model, id_item_update: int,
        field_name: str, new_value: Any, response_schema: dict[str, Any]
    ):
        """
        Функция для проверки успешного выполнения PUT-метода.

        Принимает:
        * client - Клиент для запроса
        * url - Адрес запроса
        * model - Модель для проверки сохранения данных в БД
        * id_item_update - Идентификатор обновляемой записи
        * field_name - Обновляемое поле
        * new_value - Новое значения
        * response_schema - Ожидаемая схема ответа

        Assert в случаях:
        * Если страница не найдена
        * Если страница не вернула статус 200
        * Если структура не соответствует ожидаемой
        * Если в БД не обновилась запись
        """
        old_item = getattr(model.objects.get(id=id_item_update), field_name)
        response: Response = client.put(url, {field_name: new_value})
        new_item = getattr(model.objects.get(id=id_item_update), field_name)
        self.url_get_resource(
            response=response,
            url=url,
            response_schema=response_schema
        )
        assert old_item != new_item, (
            f'Поле {field_name} в БД должно обновиться.'
        )

    def url_returns_no_content(
        self, response: Response, url: str
    ):
        """
        Функция для проверки отсутствия контента.

        Принимает:
        * response - Ответ на запрос к url
        * url - Адрес запроса

        Assert в случаях:
        * Если страница не найдена
        * Если на странице присутствует контент (статус не 204)
        """
        self._url_is_accessible(response=response, url=url)
        assert response.status_code == HTTPStatus.NO_CONTENT, (
            URL_NO_CONTENT_ERROR.format(url=url)
        )

    def url_delete_resouce(
        self, client: APIClient, url: str, model: Model, item_id: int
    ):
        """
        Функция для проверки удаления контента.

        Принимает:
        * response - Ответ на запрос к url
        * url - Адрес запроса
        * model - Модель для проверки сохранения данных в БД
        * item_id - Удаляемый объект

        Assert в случаях:
        * Если страница не найдена
        * Если на странице присутствует контент (статус не 204)
        * Если объект не удалился в БД
        """
        response: Response = client.delete(url)
        self.url_returns_no_content(response=response, url=url)
        db_items = model.objects.filter(id=item_id)
        assert not db_items, (
            'Убедитесь, что объект удаляется в БД'
        )

    def url_access_denied(
        self, client: APIClient, url: str, method: str,
        body: Optional[dict[str, Any]] = None
    ):
        """
        Функция для проверки недоступности страницы (нехватка прав).

        Принимает:
        * client - Клиент для запроса
        * url - Адрес запроса
        * method - Метод, используемый при отправке запроса
        * body - Тело запроса

        Assert в случаях:
        * Если страница не найдена
        * Если страница доступна (не работают ограничения по правам)
        """
        response: Response = getattr(client, method)(url, body)
        self._url_is_accessible(response=response, url=url)
        assert response.status_code == HTTPStatus.FORBIDDEN, (
            URL_FORBIDDEN_ERROR.format(method=method, url=url)
        )

    def url_redirects_with_found_status(
        self, client: APIClient, url: str, expected_redirect_url: str
    ):
        """
        Функция для проверки недоступности страницы (нехватка прав).

        Принимает:
        * client - Клиент для запроса
        * url - Адрес запроса
        * expected_redirect_url - Ожидаемый адрес для редиректа

        Assert в случаях:
        * Если страница не найдена
        * Если не происходит редирект
        """
        response: Response = client.get(url)
        assert response.status_code == HTTPStatus.FOUND, (
            URL_FOUND_ERROR.format(method='patch', url=url)
        )
        redirect_url = response.headers.get('Location')
        assert redirect_url == expected_redirect_url, (
            f'Проверьте, что адрес `{url}` перенаправляет на '
            f'`{expected_redirect_url}`. На текущий момент перенаправляет на '
            f'`{redirect_url}`.'
        )

    def url_reponse_count_matches_db_count(
        self, data: dict, model: Model, filters: dict[str, Any]
    ):
        """
        Функция для проверки количества объектов в ответе и БД.

        Принимает:
        * data - Ответ на запрос к url в виде словаря
        * model - Модель для проверки сохранения данных в БД
        * filters - Словарь данных, которые будут проверяться в БД

        Assert в случаях:
        * Если количество объектов на странице и в БД не совпало.
        """
        count_subscribe_DB = (
            model.objects.filter(**filters).distinct()
        )
        assert (
            count_subscribe_DB.exists()
            and len(data) == count_subscribe_DB.count()
        ), (
            'Убедитесь, что отобразились все записи.'
        )

    def url_limits_results_count(
        self, data: dict[str, Any], model: Model, filters: dict[str, Any],
        limit: int
    ):
        """
        НЕ ДЛЯ ПАГИНАЦИИ!
        Функция для проверки ограничения количества выдаваемых в объекте
        ответа внутренних объектов.

        Принимает:
        * data - Ответ на запрос к url в виде словаря
        * model - Модель для проверки сохранения данных в БД
        * filters - Словарь данных, которые будут проверяться в БД
        * limit - Требуемое количество объектов на странице

        Assert в случаях:
        * Если количество объектов на странице не соответствует limit
        """
        count_in_DB = model.objects.filter(**filters).distinct().count()
        expected_count = limit if limit < count_in_DB else count_in_DB
        assert len(data) == expected_count, (
            'Должна быть возможность изменить количество отображаемых данных'
        )

    def url_pagination_results(
        self, data: dict[str, Any], limit: int
    ):
        """
        Функция для проверки пагинации.

        Принимает:
        * data - Ответ на запрос к url в виде словаря
        * limit - Требуемое количество объектов на странице

        Assert в случаях:
        * Если не работает пагинация.
        """
        response_count: int = data.get('count', 0)
        response_results: list = data.get('results', [])
        expected_count = limit if limit < response_count else response_count
        assert len(response_results) == expected_count, (
            'Убедитесь что работает пагинация.'
        )

    def url_filters_by_query_parameters(
        self, response: Response, model: Model, filters: dict[str, Any],
        limit: Optional[int] = None
    ):
        """
        Функция для проверки фильтрации по query-параметрам.

        Принимает:
        * response - Ответ на запрос к url
        * model - Модель для проверки сохранения данных в БД
        * filters - Словарь данных, которые будут проверяться в БД
        * limit - Опционально. Требуемое количество объектов на странице

        Assert в случаях:
        * Если не работает фильтрация.
        """
        count_in_DB = model.objects.filter(**filters).distinct().count()
        data: dict = response.json()
        response_count = len(data)
        if limit:
            expected_count_results = (
                count_in_DB if count_in_DB < limit else limit
            )
        else:
            expected_count_results = count_in_DB
        assert count_in_DB == expected_count_results, (
            'Убедитесь, что фильтрация работает корректно. Ожидалось '
            f'{count_in_DB} элементов, пришло {response_count}.'
        )

    def check_db_no_changes_made(
        self, client: APIClient, url: str, model: Model
    ):
        """
        Функция для проверки сохранения дубля.

        Принимает:
        * client - Клиент для запроса
        * url - Адрес запроса
        * model - Модель для проверки сохранения данных в БД

        Assert в случаях:
        * Если страница не найдена
        * Если страница не вернула статус 400.
        * Если в БД появилась новая запись
        """
        count_in_db = model.objects.count()
        self.url_bad_request_for_invalid_data(client=client, url=url)
        new_count_in_db = model.objects.count()
        assert count_in_db == new_count_in_db, (
            'Убедитесь, что данные в БД не изменились.'
        )
