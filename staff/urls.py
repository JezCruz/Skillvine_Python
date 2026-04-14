from django.urls import path
from .views import (
    staff_dashboard,
    staff_users,
    make_user_staff,
    remove_user_staff,
    deactivate_user,
    reactivate_user,
)

urlpatterns = [
    path("", staff_dashboard, name="staff_dashboard"),
    path("users/", staff_users, name="staff_users"),
    path("users/<int:user_id>/make-staff/", make_user_staff, name="make_user_staff"),
    path("users/<int:user_id>/remove-staff/", remove_user_staff, name="remove_user_staff"),
    path("users/<int:user_id>/deactivate/", deactivate_user, name="deactivate_user"),
    path("users/<int:user_id>/reactivate/", reactivate_user, name="reactivate_user"),
]