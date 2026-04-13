from django.urls import path
from .views import (
    dashboard_home,
    settings_view,
    profile_view,
    my_learning_view,
    notifications_view,
    my_students_view,
    lessons_view,
    create_lesson_view,
)

urlpatterns = [
    path("dashboard/", dashboard_home, name="dashboard"),
    path("profile/", profile_view, name="profile"),
    path("settings/", settings_view, name="settings"),
    path("my-learning/", my_learning_view, name="my_learning"),
    path("notifications/", notifications_view, name="notifications"),
    path("my-students/", my_students_view, name="my_students"),
    path("lessons/", lessons_view, name="lessons"),
    path("lessons/create/", create_lesson_view, name="create_lesson"),
]