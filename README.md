![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)

## Содержание
- [Название проекта](#название-проекта)
- [Описание](#описание)
- [Функционал](#функционал)
- [Установка и запуск](#установка)
- [Тестирование](#тестирование)
- [Контакты](#контакты)

## Название проекта
Тестовое задание Акатосфера Django

## Описание

API маленького магазинчика со всякой всячиной. Реализован в рамках выполнения тестового задания.
Использованные технологии:
- Python 3.9
- Django 3.2.16
- Django REST framework 3.12.4

## Функционал

- Авторизация по токенам:
    - `/api/auth/register/` - регистрация
    - `/api/auth/login/` - авторизация
    - `/api/auth/logout/` - логаут
- Просмотр категорий с подкатегориями (есть пагинация):
    - `/api/category/`
- Просмотр продуктов (есть пагинация):
    - `/api/product/`
- Управление покупками для авторизованных пользователей:
    - `/api/product/{id}/shop_action/` - *POST*-добавление/обновление продукта в корзине, *DELETE*-убрать продукт из корзины
    - `/api/shopping_cart/` - *GET*-просмотр содержимого корзины (с общей суммой), *DELETE*-полная очистка корзины
- Документация:
    - `/api/swagger/`
    - `/api/redoc/`

## Установка

Перед следующими шагами убедитесь, что установленная версия Python не ниже 3.9 и не выше 3.10.
Для Windows:
```bash
python --version
```
Для Linux / macOS:
```bash
python3 --version
```

Создайте и активируйте виртуальное окружение.
Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

Установите зависимости:
```bash
pip install -r requirements.txt
```

Перейдите в директорию backend:
```bash
cd backend/
```

***ВАЖНО***: на основе файла `.env.example` в той же дирректории нужно создать файл `.env`.

Далее все команды приведины для Windows. Для Linux/MacOS используйте `python3` вместо `python`.

Выполните миграции:
```bash
python manage.py migrate
```

Наполните БД данными из фикстур:
```bash
python manage.py loaddata ../fixtures.json
```

Запустите проект:
```bash
python manage.py runserver
```

Для тестирования корзины можно воспользоваться тестовым пользователем. Для этого при включенном проекте выполните
```bash
. ../populate_db.sh
```
Данные для входа в тестового пользователя можно посмотреть в файле **populate_db**.

Для проверки функционала панели администратора следует создать суперпользователя:
```bash
python manage.py createsuperuser
```

## Тестирование

Тесты написаны на **pytest**.
Для выполнения автотестирования, находясь в папке `backend/`, выполните команду:
```bash
pytest
```

## Контакты

Код написал Раков Александр https://t.me/alexrinko
