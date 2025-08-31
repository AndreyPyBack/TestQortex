# Music Catalog API

REST API для хранения информации об исполнителях, их альбомах и песнях. Документация доступна через Swagger/Redoc. Проект упакован в Docker и использует PostgreSQL.

## Технологии
- Python 3.11, Django 5
- Django REST Framework
- drf-spectacular (Swagger/OpenAPI)
- PostgreSQL
- Docker, docker-compose

## Быстрый старт (Docker)
1. Клонировать репозиторий
```bash
git clone <repo-url>
cd PythonProject4
```
2. Запустить контейнеры
```bash
docker-compose up --build
```
3. Приложение будет доступно:
- API: http://localhost:8000/api/
- Swagger UI: http://localhost:8000/swagger/
- Redoc: http://localhost:8000/redoc/
- Админка: http://localhost:8000/admin/

По умолчанию включена загрузка seed-данных (переменная окружения `SEED=true`).

## Локальный запуск без Docker (SQLite)
```bash
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Открыть http://127.0.0.1:8000/swagger/

## Переменные окружения (docker-compose)
- POSTGRES_DB=musicdb
- POSTGRES_USER=musicuser
- POSTGRES_PASSWORD=musicpass
- POSTGRES_HOST=db
- POSTGRES_PORT=5432
- ALLOWED_HOSTS=0.0.0.0,localhost,127.0.0.1
- DJANGO_ENV=development
- SEED=true

## Миграции и суперпользователь
В контейнере веб-приложения:
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
# создать суперпользователя
docker-compose exec web python manage.py createsuperuser
```

## Seed-данные
```bash
# однократно
docker-compose exec web python manage.py seed
```
Создаются:
- Исполнители: The Beatles, Adele
- Альбомы: Abbey Road (1969), 21 (2011)
- Песни и треки с порядком в альбоме

## Структура данных (модели)
- Artist: `id`, `name`
- Album: `id`, `title`, `artist`, `release_year`
- Song: `id`, `title`
- AlbumSong (through): `album`, `song`, `track_number`

Бизнес-правила:
- Песня может быть в нескольких альбомах с разными `track_number`.
- При удалении исполнителя — удаляются его альбомы; песни остаются.

## Эндпоинты (DRF)
Базовый префикс: `/api/`
- Artists
  - GET `/artists/`
  - GET `/artists/{id}/` (возвращает альбомы и треки с `track_number`)
  - POST `/artists/`
  - PUT/PATCH `/artists/{id}/`
  - DELETE `/artists/{id}/`
- Albums
  - GET `/albums/`
  - GET `/albums/{id}/` (включая песни с `track_number`)
  - POST `/albums/`
  - PUT/PATCH `/albums/{id}/`
  - DELETE `/albums/{id}/`
- Songs
  - GET `/songs/`
  - GET `/songs/{id}/`
  - POST `/songs/`
  - PUT/PATCH `/songs/{id}/`
  - DELETE `/songs/{id}/`

Примечание: связи песен с альбомами (и их `track_number`) можно управлять через админку (`AlbumSong`) или отдельными ручными скриптами/командами.

## Примеры запросов (Postman/HTTP)
Создать исполнителя:
```http
POST http://localhost:8000/api/artists/
Content-Type: application/json

{ "name": "Nirvana" }
```
Создать альбом:
```http
POST http://localhost:8000/api/albums/
Content-Type: application/json

{ "title": "Nevermind", "artist": 1, "release_year": 1991 }
```
Создать песню:
```http
POST http://localhost:8000/api/songs/
Content-Type: application/json

{ "title": "Smells Like Teen Spirit" }
```

## Swagger
- Схема: `/api/schema/`
- Swagger UI: `/swagger/`
- Redoc: `/redoc/`

