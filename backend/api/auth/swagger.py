from drf_yasg import openapi
from django.contrib.auth.validators import UnicodeUsernameValidator


# Переменные / Поля

SCHEMA_FIRSTNAME = openapi.Schema(
    type=openapi.TYPE_STRING,
    title='Имя пользователь',
    example='Александр'
)
SCHEMA_LASTNAME = openapi.Schema(
    type=openapi.TYPE_STRING,
    title='Фамилия пользователь',
    example='Раков'
)
SCHEMA_USERNAME = openapi.Schema(
    type=openapi.TYPE_STRING,
    title='Имя пользователя',
    example='alexr',
    pattern=UnicodeUsernameValidator.regex
)
SCHEMA_EMAIL = openapi.Schema(
    type=openapi.TYPE_STRING,
    title='Электронный ящик',
    example='alexrinko@hotmai.com'
)
SCHEMA_PASSWORD = openapi.Schema(
    type=openapi.TYPE_STRING,
    title='Пароль',
    example='su4erSecret_pa$$w0rd'
)

# Сами схемы под эндпоинты

LOGIN_SCHEMA = {
    'operation_description': 'Авторизация существующего пользователя.',
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': SCHEMA_USERNAME,
            'password': SCHEMA_PASSWORD,
        },
        required=['username', 'email']
    ),
    'responses': {
        200: openapi.Response(
            description='Успешная авторизация',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'refresh': openapi.Schema(
                        type=openapi.TYPE_STRING
                    ),
                    'access': openapi.Schema(
                        type=openapi.TYPE_STRING
                    )
                }
            )
        ),
        401: openapi.Response(
            description='Неверные логин/пароль',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example=(
                            'Не найдено активной учетной записи с '
                            'указанными данными.'
                        )
                    ),
                }
            )
        ),
    }
}

LOGOUT_SCHEMA = {
    'operation_description': 'Логаут пользователя.',
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'refresh': openapi.Schema(
                type=openapi.TYPE_STRING,
                title='Токен продления'
            ),
        },
        required=['refresh']
    ),
    'responses': {
        205: openapi.Response(
            description='Успешный логаут',
        ),
        400: openapi.Response(
            description='Некорректный/повторный токен',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example=(
                            'Токен недействителен или просрочен'
                        )
                    ),
                }
            )
        ),
    }
}

REGISTER_SCHEMA = {
    'operation_description': 'Регистрация нового пользователя.',
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'first_name': SCHEMA_FIRSTNAME,
            'last_name': SCHEMA_LASTNAME,
            'username': SCHEMA_USERNAME,
            'email': SCHEMA_EMAIL,
            'password': SCHEMA_PASSWORD,
            'confirm_password': SCHEMA_PASSWORD
        },
        required=[
            'first_name', 'last_name', 'username', 'email', 'password',
            'confirm_password'
        ]
    ),
    'responses': {
        201: openapi.Response(
            description='Пользователь создан успешно',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'refresh': openapi.Schema(
                        type=openapi.TYPE_STRING
                    ),
                    'access': openapi.Schema(
                        type=openapi.TYPE_STRING
                    )
                }
            )
        ),
        400: openapi.Response(
            description='Существующие почта/логин; несовпадают пароли.',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    '{field}': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example=(
                            'Значения поля должны быть уникальны.'
                        )
                    ),
                }
            )
        ),
    }
}
