from datetime import timedelta
from pathlib import Path
from environs import Env

# Загружаем переменные из .env
env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.str("SECRET_KEY", "django-insecure-заглушка")

DEBUG = env.bool("DEBUG", False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", [])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'drf_yasg',
    'products.apps.ProductsConfig',
    'api.apps.ApiConfig',
    'api.auth.apps.AuthConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'grocery_store.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'grocery_store.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': env.str('DATABASE_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': BASE_DIR / env.str('DATABASE_NAME', 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Asia/Yekaterinburg'

USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=env.int('ACCESS_TOKEN_LIFETIME_HOURS', 12)),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=env.int('REFRESH_TOKEN_LIFETIME_DAYS', 1)),
    'ROTATE_REFRESH_TOKENS': env.bool('ROTATE_REFRESH_TOKENS', True),
    'BLACKLIST_AFTER_ROTATION': env.bool('BLACKLIST_AFTER_ROTATION', True),
}

PAGINATION = {
    'DEFAULT_PAGE_SIZE': env.int('DEFAULT_PAGE_SIZE', 10),
    'PAGE_QUERY_PARAM': 'page_size',
    'CATEGORY_MAX_PAGE_SIZE': env.int('CATEGORY_MAX_PAGE_SIZE', 100),
    'PRODUCT_MAX_PAGE_SIZE': env.int('PRODUCT_MAX_PAGE_SIZE', 50),
}
