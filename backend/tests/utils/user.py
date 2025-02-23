# Валидные данные

PASSWORD = '$echs&NDdre1z1g'
FIRST_USERNAME = 'first_user'
SECOND_USERNAME = 'second_user'
THIRD_USERNAME = 'third_user'

# Невалидные данные

TOO_LONG_EMAIL = (
    'i_have_never_seen_an_email_address_longer_than_two_hundred_and_fifty_'
    'four_characters_and_it_was_difficult_to_come_up_with_it_so_in_the_'
    'second_part_just_the_names_of_some_mail_services@yandex-google-yahoo-'
    'mailgun-protonmail-mailru-outlook-icloud-aol-neo.ru'
)
TOO_LONG_USERNAME = (
    'the-username-that-is-150-characters-long-and-should-not-pass-validation-'
    'if-the-serializer-is-configured-correctly-otherwise-the-current-test-'
    'will-fail-'
)

# Адреса страниц

URL_AUTH = '/api/auth/'
URL_REGISTER = URL_AUTH + 'register/'
URL_LOGIN = URL_AUTH + 'login/'
URL_LOGOUT = URL_AUTH + 'logout/'

# Валидные структуры

FIRST_USER = {
    'first_name': 'User',
    'last_name': 'First',
    'username': FIRST_USERNAME,
    'email': 'first@user.mail',
    'password': PASSWORD
}

SECOND_USER = {
    'first_name': 'User',
    'last_name': 'Second',
    'username': SECOND_USERNAME,
    'email': 'second@user.mail',
    'password': PASSWORD
}

THIRD_USER = {
    'first_name': 'User',
    'last_name': 'Third',
    'username': THIRD_USERNAME,
    'email': 'third@user.mail',
    'password': PASSWORD
}

# Невалидные структуры

INVALID_USER_DATA_FOR_REGISTER = [
    {
        'username': 'NoEmail',
        'first_name': 'No',
        'last_name': 'Email',
        'password': PASSWORD,
        'confirm_password': PASSWORD
    },
    {
        'email': 'no-username@user.ru',
        'first_name': 'Username',
        'last_name': 'NotProvided',
        'password': PASSWORD,
        'confirm_password': PASSWORD
    },
    {
        'username': 'NoFirstName',
        'email': 'no-first-name@user.ru',
        'last_name': 'NoFirstName',
        'password': PASSWORD,
        'confirm_password': PASSWORD
    },
    {
        'username': 'NoLastName',
        'email': 'no-last-name@user.ru',
        'first_name': 'NoLastName',
        'password': PASSWORD,
        'confirm_password': PASSWORD
    },
    {
        'username': 'NoPassword',
        'email': 'no-pasword@user.ru',
        'first_name': 'NoPassword',
        'last_name': 'NoPassword',
        'confirm_password': PASSWORD
    },
    {
        'username': 'NoConfirmPassword',
        'email': 'no-copasword@user.ru',
        'first_name': 'NoCoPassword',
        'last_name': 'NoCoPassword',
        'password': PASSWORD
    },
    {
        'username': 'IncorrectConfirmPassword',
        'email': 'incorrectPass@user.ru',
        'first_name': 'IncorrectPassword',
        'last_name': 'IncorrectPassword',
        'password': PASSWORD,
        'confirm_password': PASSWORD + PASSWORD
    },
    {
        'username': 'TooLongEmail',
        'email': TOO_LONG_EMAIL,
        'first_name': 'TooLongEmail',
        'last_name': 'TooLongEmail',
        'password': PASSWORD,
        'confirm_password': PASSWORD
    },
    {
        'username': TOO_LONG_USERNAME,
        'email': 'too-long-username@user.ru',
        'first_name': 'TooLongUsername',
        'last_name': 'TooLongUsername',
        'password': PASSWORD,
        'confirm_password': PASSWORD
    },
    {
        'username': 'InvalidU$ername',
        'email': 'invalid-username@user.ru',
        'first_name': 'Invalid',
        'last_name': 'Username',
        'password': PASSWORD,
        'confirm_password': PASSWORD
    }
]

IN_USE_USER_DATA_FOR_REGISTER = [
    {
        'email': FIRST_USER['email'],
        'username': 'EmailInUse',
        'first_name': 'Email',
        'last_name': 'InUse',
        'password': PASSWORD,
        'confirm_password': PASSWORD
    },
    {
        'email': 'username-in-use@user.ru',
        'username': FIRST_USER['username'],
        'first_name': 'Username',
        'last_name': 'InUse',
        'password': PASSWORD,
        'confirm_password': PASSWORD
    }
]

INVALID_USER_DATA_FOR_LOGIN = [
    {
        'username': SECOND_USERNAME,
        'password': 'randomPassword'
    },
    {
        'password': PASSWORD
    },
    {
        'username': SECOND_USERNAME
    }
]

# Схемы валидации данных
RESPONSE_SCHEMA_TOKEN = {
    'type': 'object',
    'properties': {
        'refresh': {'type': 'string'},
        'access': {'type': 'string'},
    },
    'required': ['refresh', 'access'],
    'additionalProperties': False
}
