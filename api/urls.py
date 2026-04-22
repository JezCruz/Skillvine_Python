from django.urls import path
from .views import (
    get_lessons,
    get_lesson,
    create_lesson,
    update_lesson,
    delete_lesson,
)

urlpatterns = [
    path('lessons/', get_lessons),
    path('lessons/create/', create_lesson),
    path('lessons/<int:id>/', get_lesson),
    path('lessons/<int:id>/update/', update_lesson),
    path('lessons/<int:id>/delete/', delete_lesson),
]