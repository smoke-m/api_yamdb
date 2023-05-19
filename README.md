

# API YamDb

## Описание

Проект 10 спринта - YamDb

**Авторы:**
- Владислав Бабаян
- Михаил Миноцкий
- Магомет Басханов

**Как запустить проект**

Клонируйте репозиторий и перейдите к нему в командной строке:

    git clone git@github.com:smoke-m/api_yamdb.git

    cd api_yamdb

Создайте и активируйте venv:

    python -m venv env
    source venv/Scripts/activate

Установите зависимости из файла requirements.txt:

    python -m pip install --upgrade pip
    pip install -r requirements.txt

Выполните миграции:

    python manage.py migrate

Запустите проект:

    python manage.py runserver

**Требования:**
- asgiref 3.6.0
- atomicwrites 1.4.1
- attrs 23.1.0
- certifi 2023.5.7
- charset-normalizer 2.0.12
- colorama 0.4.6
- Django 3.2
- django-filter 23.2
- djangorestframework 3.12.4
- djangorestframework-simplejwt 4.7.2
- idna 3.4
- iniconfig 2.0.0
- packaging 23.1
- pluggy 0.13.1
- py 1.11.0
- PyJWT 2.1.0
- pytest 6.2.4
- pytest-django 4.4.0
- pytest-pythonpath 0.7.3
- pytz 2023.3
- requests 2.26.0
- sqlparse 0.4.4
- toml 0.10.2
- urllib3 1.26.15

**Технологии:**
- Python 3.9.10
- Django 3.2
- Djangorestframework 3.12.4

**Примеры запросов API:**

Регистрация нового пользователя:

    POST http://127.0.0.1:8000/api/v1/auth/signup/

    {
        "email": "user@example.com",
        "username": "string"
    }

Пример ответа:

    {
        "email": "string",
        "username": "string"
    }

Получение JWT-токена в обмен на username и confirmation code:

    POST http://127.0.0.1:8000/api/v1/auth/token/

    {
        "text": "string",
        "image": "string",
        "group": 0
    }

Пример ответа:

    {
        "token": "string"
    }

Получить список всех категорий:

    GET http://127.0.0.1:8000/api/v1/categories/

Пример ответа:

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
    
Создать категорию:

    POST http://127.0.0.1:8000/api/v1/categories/

    {
        "name": "string",
        "slug": "string"
    }

Пример ответа:

    {
        "name": "string",
        "slug": "string"
    }

Удалить категорию:

    DELETE http://127.0.0.1:8000/api/v1/categories/{slug}/

Получить список всех жанров:

    GET http://127.0.0.1:8000/api/v1/genres/

Пример ответа:

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

Добавить жанр:

    POST http://127.0.0.1:8000/api/v1/genres/

    {
        "name": "string",
        "slug": "string"
    }
    Пример ответа
    {
        "name": "string",
        "slug": "string"
    }

Удалить жанр:

    DELETE http://127.0.0.1:8000/api/v1/genres/{slug}/

Получить список всех произведений:

    GET http://127.0.0.1:8000/api/v1/titles/

Пример ответа:

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

Добавить новое произведение:

    POST http://127.0.0.1:8000/api/v1/titles/

    {
        "name": "string",
        "year": 0,
        "description": "string",
        "genre": [
            "string"
        ],
        "category": "string"
    }

Пример ответа:

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

Информация о произведении:

    GET http://127.0.0.1:8000/api/v1/titles/{titles_id}/

   Пример ответа:

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

Обновить информацию о произведении:

    PATCH http://127.0.0.1:8000/api/v1/titles/{titles_id}/

    {
        "name": "string",
        "year": 0,
        "description": "string",
        "genre": [
            "string"
        ],
        "category": "string"
    }

Пример ответа:

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

Удалить произведение:

    DELETE http://127.0.0.1:8000/api/v1/titles/{titles_id}/


Получить список всех отзывов:

    GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/

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

Добавить новый отзыв:

    POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/

    {
        "text": "string",
        "score": 1
    }

Пример ответа:

    {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2019-08-24T14:15:22Z"
    }

Получить отзыв по ID для указанного произведения:

    GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/

Пример ответа:

    {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2019-08-24T14:15:22Z"
    }

Частично обновить отзыв по ID:

    PATCH http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/

    {
        "text": "string",
        "score": 1
    }

Пример ответа:

    {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2019-08-24T14:15:22Z"
    }

Удалить отзыв по ID:

    DELETE http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/

Получить список всех комментариев к отзыву по ID:

    GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/

Пример ответа:

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

Добавить новый комментарий для отзыва:

    POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/

    {
        "text": "string"
    }
   Пример ответа:

    {
        "id": 0,
        "text": "string",
        "author": "string",
        "pub_date": "2019-08-24T14:15:22Z"
    }

Получить комментарий для отзыва по ID:

    GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/

Пример ответа:

    {
        "id": 0,
        "text": "string",
        "author": "string",
        "pub_date": "2019-08-24T14:15:22Z"
    }

Частично обновить комментарий к отзыву по ID:

    PATCH http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/

    {
        "text": "string"
    }
Пример ответа:

    {
        "id": 0,
        "text": "string",
        "author": "string",
        "pub_date": "2019-08-24T14:15:22Z"
    }

Удалить комментарий к отзыву по ID:

    DELETE http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/

Получить список всех пользователей:

    GET http://127.0.0.1:8000/api/v1/users/

Пример ответа:

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

Добавить нового пользователя:

    POST http://127.0.0.1:8000/api/v1/users/
    
    {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
    }

Пример ответа:

    {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
    }

Получить пользователя по username:

    GET http://127.0.0.1:8000/api/v1/users/{username}/

Пример ответа:

    {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
    }

Изменить данные пользователя по username:

    PATCH http://127.0.0.1:8000/api/v1/users/{username}/

    {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
    }

Пример ответа:

    {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
    }

Удалить пользователя по username:

    DELETE http://127.0.0.1:8000/api/v1/users/{username}/

Получить данные своей учетной записи:

    GET http://127.0.0.1:8000/api/v1/users/me/

Пример ответа:

    {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
    }

Изменить данные своей учетной записи:

    PATCH http://127.0.0.1:8000/api/v1/users/me/

    {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
    }

Пример ответа:

    {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
    }

Copyright (c) 2023 

[Владислав Бабаян](https://github.com/doberman-ghost) **|** [Михаил Миноцкий](https://github.com/smoke-m) **|** [Магомет Басханов](https://github.com/MAGFRG)
