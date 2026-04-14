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
    browse_lessons_view,
    enroll_lesson_view,
    wallet_view,
    search_view,
    teacher_profile_popup_view,
    toggle_follow_teacher_view,
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
    path("browse-lessons/", browse_lessons_view, name="browse_lessons"),
    path("browse-lessons/<int:lesson_id>/enroll/", enroll_lesson_view, name="enroll_lesson"),
    path("wallet/", wallet_view, name="wallet"),
    path("search/", search_view, name="search"),
    path("teachers/<int:teacher_id>/popup/", teacher_profile_popup_view, name="teacher_profile_popup"),
    path("teachers/<int:teacher_id>/follow/", toggle_follow_teacher_view, name="toggle_follow_teacher"),
]