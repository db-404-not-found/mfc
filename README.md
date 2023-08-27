# МФЦ помощник

## Описание

Веб-приложение выступает интеллектуальным помощником оператора и позволяет отправлять запросы по оформлению документов и другой деятельности сотрудника МФЦ и получить релевантный ответ в кратчайшие сроки. Стек технологий:

<a href="https://github.com/Ileriayo/markdown-badges">
  <p align="center">
    <img alt="Python" src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"/>
    <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi"/>
    <img alt="Docker" src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white"/>
    <img alt="Postgres" src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white"/>
    <img alt="Nginx" src="https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white"/>
    <img alt="GitHub" src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/>
    <img alt="GitHub Actions" src="https://img.shields.io/badge/githubactions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white"/>
    <img alt="RabbitMQ" src="https://img.shields.io/badge/Rabbitmq-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white"/>
    <img alt="MLFlow" src="https://img.shields.io/badge/mlflow-%23d9ead3.svg?style=for-the-badge&logo=numpy&logoColor=blue"/>
    <img alt="Grafana" src="https://img.shields.io/badge/grafana-%23F46800.svg?style=for-the-badge&logo=grafana&logoColor=white"/>
    <img alt="Prometheus" src="https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=Prometheus&logoColor=white"/>
  </p>
</a>

## Установка

Для использования проекта необходимо скачать исходный код:

```bash
git clone https://github.com/db-404-not-found/mfc
```

## Настройка

Для конфигурации проекта необходимо создать файл с переменными оружения из `.env.dev`.

Если планируете использовать базу данных не из `docker-compose.yaml` не забудьте переопределить `POSTGRES_HOST` и `POSTGRES_PORT`.

```bash
cp .env.dev .env
```

```bash
POSTGRES_USER     # пользователь для подключения к базе данных
POSTGRES_PASSWORD # пароль для подключения к базе данных
POSTGRES_HOST     # домен или IP-адрес базы данных
POSTGRES_DB       # база данных проекта
POSTGRES_PORT     # порт базы данных
```

## Запуск

### Docker

Для запуска рекомендуется использовать `docker compose`.

```bash
docker compose up --build -d
```

### Локально

Требования: версия Python >= 3.11.

Для запуска проекта локально необходимо предустановить в систему `poetry`

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip poetry
poetry install --no-root
poetry run gunicorn -c backend/gunicorn.conf.py backend.main:app
```

### Миграция базы данных

Для применения миграции после запуска контейнеров выполните

```bash
docker compose exec backend alembic -c backend/alembic.ini upgrade head
```

Для создания новой миграции автоматически

```bash
docker compose exec backend alembic -c backend/alembic.ini revision --autogenerate -m "New migration name"
```

## Использование

После запуска проекта локально по адресу `http://127.0.0.1/` откроется лендинг с формой для тестирования проекта, а по адресу `http://127.0.0.1/docs` будет доступен интерфейс Swagger для использования API проекта.

- `GET  /api/monitoring/ping` - проверка работоспособности сервера
- `POST /api/v1/inference` - отправляет запрос в обработку моделью или сразу возвращает результат на известный запрос
- `GET  /api/v1/tasks/{task_id}` - получение информации о запросе, который есть в системе по `task_id`
