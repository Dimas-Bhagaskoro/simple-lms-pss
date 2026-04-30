from ninja import Router, Schema
from typing import List
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import Course, Enrollment, Progress, Lesson
from users.api import AuthBearer

router = Router()
User = get_user_model()

# =====================
# SCHEMA
# =====================
class CourseSchema(Schema):
    id: int
    title: str
    description: str

class CourseCreateSchema(Schema):
    title: str
    description: str

# =====================
# PUBLIC
# =====================

@router.get("/", response=List[CourseSchema])
def list_courses(request, limit: int = 10):
    return Course.objects.all()[:limit]

@router.get("/{course_id}", response=CourseSchema)
def get_course(request, course_id: int):
    return get_object_or_404(Course, id=course_id)

# =====================
# PROTECTED
# =====================

@router.post("/", auth=AuthBearer())
def create_course(request, data: CourseCreateSchema):
    user = User.objects.get(id=request.auth["user_id"])

    if user.role != "instructor":
        return {"error": "Hanya instructor"}

    course = Course.objects.create(
        title=data.title,
        description=data.description,
        instructor=user
    )

    return {"id": course.id, "title": course.title}

@router.patch("/{course_id}", auth=AuthBearer())
def update_course(request, course_id: int, data: CourseCreateSchema):
    user = User.objects.get(id=request.auth["user_id"])
    course = get_object_or_404(Course, id=course_id)

    if course.instructor_id != user.id:
        return {"error": "Bukan pemilik"}

    course.title = data.title
    course.description = data.description
    course.save()

    return {"message": "Updated"}

@router.delete("/{course_id}", auth=AuthBearer())
def delete_course(request, course_id: int):
    user = User.objects.get(id=request.auth["user_id"])
    course = get_object_or_404(Course, id=course_id)

    if user.role != "admin":
        return {"error": "Hanya admin"}

    course.delete()
    return {"message": "Deleted"}

# =====================
# ENROLLMENTS
# =====================

@router.post("/enrollments/{course_id}", auth=AuthBearer())
def enroll_course(request, course_id: int):
    user = User.objects.get(id=request.auth["user_id"])

    if user.role != "student":
        return {"error": "Hanya student"}

    enrollment, created = Enrollment.objects.get_or_create(
        student=user,
        course_id=course_id
    )

    if not created:
        return {"message": "Sudah terdaftar"}

    return {"message": "Berhasil enroll"}

@router.get("/enrollments/my-courses", auth=AuthBearer())
def my_courses(request):
    user = User.objects.get(id=request.auth["user_id"])

    enrollments = Enrollment.objects.filter(student=user)

    return [
        {
            "id": e.course.id,
            "title": e.course.title,
            "description": e.course.description
        }
        for e in enrollments
    ]

@router.post("/enrollments/{enrollment_id}/progress", auth=AuthBearer())
def mark_progress(request, enrollment_id: int, lesson_id: int):
    user = User.objects.get(id=request.auth["user_id"])

    enrollment = get_object_or_404(Enrollment, id=enrollment_id)

    if enrollment.student_id != user.id:
        return {"error": "Bukan enrollment kamu"}

    lesson = get_object_or_404(Lesson, id=lesson_id)

    if lesson.course_id != enrollment.course_id:
        return {"error": "Lesson tidak sesuai"}

    progress, _ = Progress.objects.get_or_create(
        enrollment=enrollment,
        lesson=lesson
    )

    progress.is_completed = True
    progress.save()

    return {"message": "Lesson selesai 🎉"}