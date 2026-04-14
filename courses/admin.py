from django.contrib import admin
from .models import User, Category, Course, Lesson, Enrollment, Progress

# Agar kita bisa nambah Lesson langsung di halaman Course (Hemat waktu!)
class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category') # Kolom yang tampil
    list_filter = ('category', 'instructor')          # Fitur filter di kanan
    search_fields = ('title',)                        # Fitur pencarian
    inlines = [LessonInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')

# Daftarkan model lainnya
admin.site.register(User)
admin.site.register(Enrollment)
admin.site.register(Progress)