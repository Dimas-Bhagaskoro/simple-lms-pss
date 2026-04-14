# 🎓 Simple LMS

Simple Learning Management System (LMS) project built with **Django**, **Docker**, and **PostgreSQL**.

Project ini dikembangkan bertahap dari setup dasar hingga implementasi fitur LMS lengkap beserta optimasi query database.

---

## 🚀 Tech Stack

- Django
- PostgreSQL
- Docker
- Docker Compose

---

## 📂 Project Structure

simple-lms/
├── config/
├── courses/
│   ├── fixtures/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   └── ...
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── .env
├── manage.py
└── README.md

---

## ⚙️ Setup & Run Project

### Clone Repository

git clone <URL-REPO-KAMU>
cd simple-lms

### Setup Environment

cp .env.example .env

### Build & Run

docker compose up --build -d

### Migration

docker compose exec web python manage.py migrate

### Create Superuser

docker compose exec web python manage.py createsuperuser

### Load Initial Data

docker compose exec web python manage.py loaddata initial_data

---

## 🌐 Access Application

http://localhost:8000

Admin Panel:

http://localhost:8000/admin

---

## ✅ Features

### Progress 1

- Dockerized Django app
- PostgreSQL integration
- Environment configuration
- Running development server

### Progress 2

- Custom User model (Admin / Instructor / Student)
- Category hierarchy
- Course management
- Ordered lessons
- Enrollment system
- Progress tracking

---

## ⚡ Query Optimization

Using `select_related()` to solve N+1 query issue.

| Scenario | Query | Total |
|----------|-------|------|
| Default | Course.objects.all() | 2+ |
| Optimized | Course.objects.for_listing() | 1 |
