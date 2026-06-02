from ninja import Router, Schema
from typing import List
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.cache import cache
from .rate_limit import rate_limit

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

    rate_limit(request)
    
    cache_key = f"courses_list_{limit}"

    courses = cache.get(cache_key)

    if courses is None:
        courses = list(
            Course.objects.all().values(
                "id",
                "title",
                "description"
            )[:limit]
        )

        cache.set(cache_key, courses, timeout=300)

    return courses

@router.get("/{course_id}", response=CourseSchema)
def get_course(request, course_id: int):

    cache_key = f"course_{course_id}"

    course = cache.get(cache_key)

    if course is None:

        course_obj = get_object_or_404(Course, id=course_id)

        course = {
            "id": course_obj.id,
            "title": course_obj.title,
            "description": course_obj.description,
        }

        cache.set(cache_key, course, timeout=300)

    return course

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
    cache.delete_pattern("courses_list_*")
    
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

    cache.delete_pattern("courses_list_*")
    cache.delete(f"course_{course_id}")

    return {"message": "Updated"}

@router.delete("/{course_id}", auth=AuthBearer())
def delete_course(request, course_id: int):
    user = User.objects.get(id=request.auth["user_id"])
    course = get_object_or_404(Course, id=course_id)

    if user.role != "admin":
        return {"error": "Hanya admin"}

    cache.delete_pattern("courses_list_*")
    cache.delete(f"course_{course_id}")

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