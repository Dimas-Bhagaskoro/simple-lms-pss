# Simple LMS

Simple Learning Management System (LMS) project built with Django, Docker, and PostgreSQL.

---

## 🚀 Tech Stack

* Django
* PostgreSQL
* Docker & Docker Compose

---

## 📂 Project Structure

```
simple-lms/
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── requirements.txt
├── manage.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── README.md
```

---

## ⚙️ Setup & Run Project

### 1. Clone Repository

```bash
git clone <URL-REPO-KAMU>
cd simple-lms
```

### 2. Setup Environment Variables

Copy file `.env.example` menjadi `.env`:

```bash
cp .env.example .env
```

---

### 3. Build & Run Docker

```bash
docker compose up --build
```

---

### 4. Run Migration

```bash
docker compose exec web python manage.py migrate
```

---

### 5. Akses Aplikasi

Buka browser:

```
http://localhost:8000
```

---

## 🔐 Environment Variables

| Variable          | Description                  |
| ----------------- | ---------------------------- |
| DEBUG             | Mode debug Django            |
| SECRET_KEY        | Secret key Django            |
| ALLOWED_HOSTS     | Host yang diizinkan          |
| POSTGRES_DB       | Nama database                |
| POSTGRES_USER     | Username database            |
| POSTGRES_PASSWORD | Password database            |
| POSTGRES_HOST     | Host database (gunakan `db`) |
| POSTGRES_PORT     | Port PostgreSQL              |

---

## 📸 Screenshot

![Django Welcome](screenshots/django-welcome.jpg)

---

## ✅ Features (Current Progress)

* Dockerized Django application
* PostgreSQL database integration
* Environment-based configuration
* Django development server running

---

## 📌 Notes

* Gunakan Docker Desktop untuk menjalankan project
* Pastikan port 8000 dan 5432 tidak digunakan aplikasi lain
