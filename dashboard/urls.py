from django.urls import path
from .views import dashboard_home, settings_view, profile_view

urlpatterns = [
    path("dashboard/", dashboard_home, name="dashboard"),
    path("settings/", settings_view, name="settings"),
    path("profile/", profile_view, name="profile"),
]