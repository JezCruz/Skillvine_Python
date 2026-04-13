from django.contrib import admin
from .models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "teacher", "category", "status", "created_at")
    list_filter = ("category", "status")
    search_fields = ("title", "teacher__email", "teacher__full_name")