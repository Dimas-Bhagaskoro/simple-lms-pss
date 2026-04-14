from django.db import models
from django.contrib.auth.models import AbstractUser

# --- 1. CUSTOM MANAGERS (Untuk Optimasi Query) ---

class CourseQuerySet(models.QuerySet):
    def for_listing(self):
        """Mengambil instructor dan category dalam 1 query saja (mencegah N+1)"""
        return self.select_related('instructor', 'category')

class EnrollmentQuerySet(models.QuerySet):
    def for_student_dashboard(self):
        """Mengambil data course dan progress sekaligus"""
        return self.select_related('course').prefetch_related('progress_tracking')

# --- 2. MODELS ---

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('instructor', 'Instructor'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

class Category(models.Model):
    name = models.CharField(max_length=100)
    # Self-referencing (Category bisa punya Parent Category)
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories'
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.parent.name} > {self.name}" if self.parent else self.name

class Course(models.Model):
    title = models.CharField(max_length=200)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'instructor'})
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    
    # Menghubungkan Manager ke Model
    objects = CourseQuerySet.as_manager()

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField() # Untuk ordering

    class Meta:
        ordering = ['order']
        # Mencegah ada nomor urut lesson yang sama di dalam satu course
        unique_together = ('course', 'order')

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    objects = EnrollmentQuerySet.as_manager()

    class Meta:
        # User tidak bisa daftar ke course yang sama dua kali
        unique_together = ('student', 'course')

class Progress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='progress_tracking')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)