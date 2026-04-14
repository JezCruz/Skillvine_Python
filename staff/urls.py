from django.urls import path
from .views import staff_dashboard, staff_users

urlpatterns = [
    path("", staff_dashboard, name="staff_dashboard"),
    path("users/", staff_users, name="staff_users"),
]