API YAMDB
Описание
api_yamdb - 10ый спринт.

Авторы:
Владислав Бабаян
Михаил Миноцкий
Магомет Басханов

Как запустить проект

Клонируйте репозиторий и перейдите к нему в командной строке:
git clone git@github.com:smoke-m/api_yamdb.git
cd api_yamdb

Создайте и активируйте venv:
python -m venv env
source venv/Scripts/activate

Установить зависимости из файла requirements.txt:
python -m pip install --upgrade pip
pip install -r requirements.txt

Выполнять миграции:
python manage.py migrate

Запустить проект:
python manage.py runserver
Требования
asgiref==3.6.0
atomicwrites==1.4.1
attrs==23.1.0
certifi==2023.5.7
charset-normalizer==2.0.12
colorama==0.4.6
Django==3.2
django-filter==23.2
djangorestframework==3.12.4
djangorestframework-simplejwt==4.7.2
idna==3.4
iniconfig==2.0.0
packaging==23.1
pluggy==0.13.1
py==1.11.0
PyJWT==2.1.0
pytest==6.2.4
pytest-django==4.4.0
pytest-pythonpath==0.7.3
pytz==2023.3
requests==2.26.0
sqlparse==0.4.4
toml==0.10.2
urllib3==1.26.15

Технологии
Python 3.9.10
Django 3.2
Djangorestframework 3.12.4

Примеры запросов API

POST http://127.0.0.1:8000/api/v1/auth/signup/
Регистрация нового пользователя
{
    "email": "user@example.com",
    "username": "string"
}
Пример ответа
{
    "email": "string",
    "username": "string"
}

POST http://127.0.0.1:8000/api/v1/auth/token/
Получение JWT-токена в обмен на username и confirmation code.
{
    "text": "string",
    "image": "string",
    "group": 0
}
Пример ответа
{
    "token": "string"
}

GET http://127.0.0.1:8000/api/v1/categories/
Получить список всех категорий
Пример ответа
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
        {
            "name": "string",
            "slug": "string"
        }
    ]
}

POST http://127.0.0.1:8000/api/v1/categories/
Создать категорию.
{
    "name": "string",
    "slug": "string"
}
Пример ответа
{
    "name": "string",
    "slug": "string"
}

DELETE http://127.0.0.1:8000/api/v1/categories/{slug}/
Удалить категорию.

GET http://127.0.0.1:8000/api/v1/genres/
Получить список всех жанров.
Пример ответа
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
        {
            "name": "string",
            "slug": "string"
        }
    ]
}

POST http://127.0.0.1:8000/api/v1/genres/
Добавить жанр.
{
    "name": "string",
    "slug": "string"
}
Пример ответа
{
    "name": "string",
    "slug": "string"
}

DELETE http://127.0.0.1:8000/api/v1/genres/{slug}/
Удалить жанр.

GET http://127.0.0.1:8000/api/v1/titles/
Получить список всех Произведений.
Пример ответа
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
        {
            "id": 0,
            "name": "string",
            "year": 0,
            "rating": 0,
            "description": "string",
            "genre": [
                {
                    "name": "string",
                    "slug": "string"
                }
            ],
            "category": {
                "name": "string",
                "slug": "string"
            }
        }
    ]
}

POST http://127.0.0.1:8000/api/v1/titles/
Добавить новое произведение.
{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
        "string"
    ],
    "category": "string"
}
Пример ответа
{
    "id": 0,
    "name": "string",
    "year": 0,
    "rating": 0,
    "description": "string",
    "genre": [
        {
            "name": "string",
            "slug": "string"
        }
    ],
    "category": {
        "name": "string",
        "slug": "string"
    }
}

GET http://127.0.0.1:8000/api/v1/titles/{titles_id}/
Информация о произведении
Пример ответа
{
    "id": 0,
    "name": "string",
    "year": 0,
    "rating": 0,
    "description": "string",
    "genre": [
        {
            "name": "string",
            "slug": "string"
        }
    ],
    "category": {
        "name": "string",
        "slug": "string"
    }
}

PATCH http://127.0.0.1:8000/api/v1/titles/{titles_id}/
Обновить информацию о произведении
{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
        "string"
    ],
    "category": "string"
}
Пример ответа
{
    "id": 0,
    "name": "string",
    "year": 0,
    "rating": 0,
    "description": "string",
    "genre": [
        {
            "name": "string",
            "slug": "string"
        }
    ],
    "category": {
        "name": "string",
        "slug": "string"
    }
}

DELITE http://127.0.0.1:8000/api/v1/titles/{titles_id}/
Удалить произведение.

GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
Получить список всех отзывов.
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
        {
            "id": 0,
            "text": "string",
            "author": "string",
            "score": 1,
            "pub_date": "2019-08-24T14:15:22Z"
        }
    ]
}

POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
Добавить новый отзыв.
{
    "text": "string",
    "score": 1
}
Пример ответа
{
    "id": 0,
    "text": "string",
    "author": "string",
    "score": 1,
    "pub_date": "2019-08-24T14:15:22Z"
}

GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
Получить отзыв по id для указанного произведения.
Пример ответа
{
    "id": 0,
    "text": "string",
    "author": "string",
    "score": 1,
    "pub_date": "2019-08-24T14:15:22Z"
}

PATCH http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
Частично обновить отзыв по id.
{
    "text": "string",
    "score": 1
}
Пример ответа
{
    "id": 0,
    "text": "string",
    "author": "string",
    "score": 1,
    "pub_date": "2019-08-24T14:15:22Z"
}

DELETE http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
Удалить отзыв по id.

GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
Получить список всех комментариев к отзыву по id
Пример ответа
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
        {
            "id": 0,
            "text": "string",
            "author": "string",
            "pub_date": "2019-08-24T14:15:22Z"
        }
    ]
}

POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
Добавить новый комментарий для отзыва.
{
    "text": "string"
}
Пример ответа
{
    "id": 0,
    "text": "string",
    "author": "string",
    "pub_date": "2019-08-24T14:15:22Z"
}

GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
Получить комментарий для отзыва по id.
Пример ответа
{
    "id": 0,
    "text": "string",
    "author": "string",
    "pub_date": "2019-08-24T14:15:22Z"
}

PATCH http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
Частично обновить комментарий к отзыву по id.
{
    "text": "string"
}
Пример ответа
{
    "id": 0,
    "text": "string",
    "author": "string",
    "pub_date": "2019-08-24T14:15:22Z"
}

DELETE http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
Удалить комментарий к отзыву по id.

GET http://127.0.0.1:8000/api/v1/users/
Получить список всех пользователей.
Пример ответа
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
        {
            "username": "string",
            "email": "user@example.com",
            "first_name": "string",
            "last_name": "string",
            "bio": "string",
            "role": "user"
        }
    ]
}

POST http://127.0.0.1:8000/api/v1/users/
Добавить нового пользователя.
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
Пример ответа
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}

GET http://127.0.0.1:8000/api/v1/users/{username}/
Получить пользователя по username.
Пример ответа
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}

PATCH http://127.0.0.1:8000/api/v1/users/{username}/
Изменить данные пользователя по username.
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
Пример ответа
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}

DELETE http://127.0.0.1:8000/api/v1/users/{username}/
Удалить пользователя по username.

GET http://127.0.0.1:8000/api/v1/users/me/
Получить данные своей учетной записи
Пример ответа
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}

PATCH http://127.0.0.1:8000/api/v1/users/me/
Изменить данные своей учетной записи
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
Пример ответа
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}

Copyright (c) 2023 
Владислав Бабаян
Михаил Миноцкий
Магомет Басханов