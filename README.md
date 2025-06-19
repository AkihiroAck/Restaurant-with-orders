# 🍽 Restaurant API

Этот проект — REST API для управления **блюдами** и **заказами** ресторана. Реализован с помощью **Django** и **Django REST Framework**, запускается в контейнерах Docker.

---

## 🚀 Быстрый запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/ваш-профиль/Restaurant-with-orders.git
cd Restaurant-with-orders
````

### 2. Создать файл `.env`

Пример содержимого:

```env
SECRET_KEY=django-insecure-0^m1js03lc3x!r-c8yr)wf4+w+&7i39l#5n@i3h=l7v$fr-9f3
POSTGRES_ENGINE=django.db.backends.postgresql
POSTGRES_DB=db_name
POSTGRES_USER=db_user
POSTGRES_PASSWORD=db_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE=postgres
```

### 3. Запустить проект через Docker Compose

```bash
docker-compose up --build
```

После запуска:

* API будет доступен на: **[http://localhost:8080/](http://localhost:8080/)**
* База данных PostgreSQL на порту: **5000**
* Админ-панель Adminer: **[http://localhost/80](http://localhost/80)**

---

## ⚙️ Используемые порты

| Сервис     | В контейнере | На хосте | Назначение         |
| ---------- | ------------ | -------- | ------------------ |
| Django     | `8000`       | `8080`   | REST API           |
| PostgreSQL | `5432`       | `5000`   | СУБД PostgreSQL    |
| Adminer    | `8080`       | `80`     | Веб-интерфейс к БД |

ℹ️ Для изменения портов и других параметров — [редактируйте Docker Compose ↓](#структура_docker_compose)

---

## 🔧 Структура API

### 📘 Блюда

#### `GET /dishes/`

Получить список всех блюд.

#### `POST /dishes/`

Создать новое блюдо.
Пример запроса:

```json
{
  "name": "Пицца Маргарита",
  "description": "Томатный соус, сыр, базилик",
  "price": "750.00",
  "category": "Пицца"
}
```

#### `DELETE /dishes/{id}/`

Удалить блюдо по ID.

---

### 📦 Заказы

#### `GET /orders/`

Получить список заказов.

#### `POST /orders/`

Создать новый заказ.
Пример:

```json
{
  "customer_name": "Иван Петров",
  "dishes": [1, 2]
}
```

#### `PATCH /orders/{id}/`

Обновить заказ (например, изменить блюда или customer_name).

#### `DELETE /orders/{id}/`

Отменить заказ. 
Если его статус — `PENDING`, он станет `CANCELLED`.
Иначе, ошибка 400.

---

### 🔄 Обновление статуса заказа

#### `PATCH /orders/{id}/status/`

Обновить статус.
Допустимая последовательность:

* `PENDING` → `PREPARING` → `DELIVERING` → `COMPLETED`

Пример запроса:

```json
{
  "status": "PREPARING"
}
```

Недопустимый переход, например, с `PENDING` на `COMPLETED`, вызовет ошибку.

---

## 🛠 Технологии

* Python 3.12.10
* Django 5.2.3
* Django REST Framework 3.16.0
* PostgreSQL 17.4
* Docker / Docker Compose

---

## 🧱 Структура Docker Compose

```yaml
services:
  web:
    build: ./restaurant
    container_name: django
    volumes:
      - ./restaurant/:/usr/src/app/
    ports:
      - 8080:8000
    env_file:
      - .env
    depends_on:
      - db

  db:
    image: postgres:17.4
    restart: always
    container_name: postgresql
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - 5000:5432

  adminer:
    image: adminer
    restart: always
    container_name: adminer
    ports:
      - 80:8080

volumes:
  postgres_data:
```

---

## ✅ Примечания

* Заказ нельзя создать без блюд.
* Удаление блюда удаляет его из всех заказов.
* При создании заказа, его status по умолчанию `PENDING`.
* Отменить можно только заказ в статусе `PENDING`.
