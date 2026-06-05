# 🎓 Simple LMS

Simple Learning Management System (LMS) project built with **Django**, **Django Ninja**, **JWT Authentication**, **Docker**, and **PostgreSQL**.

Project ini dikembangkan bertahap dari setup dasar hingga implementasi REST API lengkap dengan authentication dan role-based authorization.

---

## 🚀 Tech Stack

- Django
- Django Ninja
- PostgreSQL
- Docker
- Docker Compose
- JWT (JSON Web Token)
- Pydantic (Schema validation)

---

## 📂 Project Structure

simple-lms/
├── config/
├── courses/
│ ├── migrations/
│ ├── models.py
│ ├── api.py
│ └── ...
├── users/
│ ├── api.py
│ └── ...
├── screenshots/
├── docker-compose.yml
├── Dockerfile
├── .env
├── manage.py
└── README.md


---

## ⚙️ Setup & Run Project

### Clone Repository
git clone https://github.com/Dimas-Bhagaskoro/simple-lms-pss.git
cd simple-lms

### Setup Environment
cp .env.example .env

### Build & Run
docker compose up --build -d

### Migration
docker compose exec web python manage.py migrate

### Create Superuser
docker compose exec web python manage.py createsuperuser


---

## 🌐 Access Application

- Main App: http://localhost:8000  
- Admin Panel: http://localhost:8000/admin  
- API Docs (Swagger): http://localhost:8000/api/docs  

---

## ✅ Features

### 🔹 Progress 1
- Dockerized Django app
- PostgreSQL integration
- Environment configuration

### 🔹 Progress 2
- Custom User model (Admin / Instructor / Student)
- Category & Course management
- Lesson system
- Enrollment system
- Progress tracking
- Query optimization (`select_related`, `prefetch_related`)

### 🔹 Progress 3 (REST API)

#### 🔐 Authentication (JWT)
- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/refresh`
- `GET /api/auth/me`
- `PUT /api/auth/me`

---

#### 📚 Courses API

**Public**
- `GET /api/courses`
- `GET /api/courses/{id}`

**Protected**
- `POST /api/courses` (Instructor)
- `PATCH /api/courses/{id}` (Owner)
- `DELETE /api/courses/{id}` (Admin)

---

#### 🎓 Enrollment API

- `POST /api/courses/enroll`
- `GET /api/courses/my-courses`
- `POST /api/courses/enrollments/{id}/progress`

---

## 🛡️ Authentication System

- JWT Access Token
- Token validation middleware
- Password hashing (Django default)

Gunakan header berikut untuk endpoint protected:


---

## 🔐 Role-Based Access Control (RBAC)

- **Admin** → bisa delete course
- **Instructor** → bisa create & update course
- **Student** → bisa enroll & akses course

---

## 📑 API Documentation

Swagger UI tersedia di:
http://localhost:8000/api/docs


---

## 🧪 API Testing (Postman)

API telah diuji menggunakan Postman.

Collection berisi:
- Auth (login, register, me)
- Courses (CRUD)
- Enrollment
- Progress tracking

---

### 🔹 Progress 4 (Advanced Features & Integration)

#### ⚡ Redis Integration

Redis digunakan untuk meningkatkan performa aplikasi dengan menyimpan data yang sering diakses.

Implemented Features:
- Course List Caching
- Course Detail Caching
- Cache Invalidation Strategy
- Rate Limiting (60 requests/minute)

---

#### 🍃 MongoDB Integration

MongoDB digunakan untuk menyimpan data non-relasional seperti activity logs dan learning analytics.

##### Activity Logs

Mencatat aktivitas user saat melakukan enrollment course.

Contoh data:

```json
{
  "user_id": 5,
  "action": "enroll_course",
  "course_id": 3
}
```

##### Learning Analytics

Mencatat aktivitas pembelajaran student.

Contoh data:

```json
{
  "user_id": 5,
  "course_id": 3,
  "lesson_id": 2,
  "action": "lesson_completed"
}
```

##### Aggregation Reports

MongoDB Aggregation digunakan untuk menghasilkan laporan analytics berdasarkan aktivitas pembelajaran student.

---

#### 🐇 RabbitMQ Integration

RabbitMQ digunakan sebagai message broker antara Django dan Celery.

Flow:

Django API  
↓  
RabbitMQ  
↓  
Celery Worker  
↓  
Task Execution

---

#### 🚀 Celery Tasks

Asynchronous task processing menggunakan Celery.

Implemented Tasks:

- send_enrollment_email
- generate_certificate
- export_course_report
- update_course_statistics

---

#### ⏰ Celery Beat

Celery Beat digunakan untuk menjalankan scheduled task secara otomatis.

Scheduled Task:

- update_course_statistics (setiap 60 detik)

---

#### 📊 Flower Monitoring

Flower digunakan untuk monitoring Celery Worker dan task execution.

Access:

http://localhost:5555

Features:
- Worker Monitoring
- Task Monitoring
- Success / Failure Tracking
- Queue Monitoring

---

## 🏗️ Architecture Diagram

```mermaid
graph TD

    User --> Django

    Django --> PostgreSQL
    Django --> Redis
    Django --> MongoDB

    Django --> RabbitMQ

    RabbitMQ --> CeleryWorker
    RabbitMQ --> CeleryBeat

    CeleryWorker --> Flower

    CeleryWorker --> SendEnrollmentEmail
    CeleryWorker --> GenerateCertificate
    CeleryWorker --> ExportCourseReport
    CeleryWorker --> UpdateCourseStatistics
```

---

## ⚡ Caching Strategy

Redis digunakan untuk meningkatkan performa aplikasi dengan mengurangi query berulang ke PostgreSQL.

### Course List Cache

Daftar course disimpan di Redis sehingga request berikutnya dapat langsung mengambil data dari cache tanpa melakukan query ulang ke database.

### Course Detail Cache

Detail course disimpan di Redis berdasarkan course ID untuk mempercepat akses data.

### Cache Invalidation

Cache akan dihapus ketika data course mengalami perubahan (create, update, delete) sehingga data yang ditampilkan tetap konsisten dengan database.

---

## 🔄 Celery Task Flow

### Enrollment Email

Student Enroll  
↓  
Django API  
↓  
RabbitMQ  
↓  
Celery Worker  
↓  
send_enrollment_email

---

### Certificate Generation

Course Completion  
↓  
Django API  
↓  
RabbitMQ  
↓  
Celery Worker  
↓  
generate_certificate

---

### Course Report Export

Admin Request  
↓  
RabbitMQ  
↓  
Celery Worker  
↓  
export_course_report

---

### Scheduled Statistics Update

Celery Beat  
↓  
RabbitMQ  
↓  
Celery Worker  
↓  
update_course_statistics

---

## 📟 Redis CLI Commands

Masuk ke Redis CLI:

```bash
docker exec -it simple_lms_redis redis-cli
```

Melihat seluruh key:

```bash
KEYS *
```

Melihat isi cache:

```bash
GET key_name
```

Menghapus cache tertentu:

```bash
DEL key_name
```

Melihat jumlah key dalam database Redis:

```bash
DBSIZE
```

Melihat informasi dan statistik Redis:

```bash
INFO
```

Keluar dari Redis CLI:

```bash
exit
```

---

## ⚡ Query Optimization

Menggunakan `select_related()` dan `prefetch_related()` untuk menghindari N+1 query problem.

| Scenario | Query | Total |
|----------|------|------|
| Default | Course.objects.all() | Multiple |
| Optimized | Course.objects.for_listing() | 1 |

## 📸 Screenshots

![Django](./screenshots/django-welcome.jpeg)
![Swagger](./screenshots/swagger-documentation.jpg)
![Postman](./screenshots/postman-dashboard.png)
![Courses](./screenshots/course.jpg)
![Flower](./screenshots/flower-task.png)
![RabbitMQ](./screenshots/rabbitMQ.png)