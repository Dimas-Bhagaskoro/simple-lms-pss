from ninja import Router
from .models import Course

router = Router()

@router.get("/courses")
def list_courses(request):
    courses = Course.objects.for_listing()
    return [
        {
            "id": c.id,
            "title": c.title,
            "instructor": c.instructor.username,
            "category": c.category.name,
        }
        for c in courses
    ]