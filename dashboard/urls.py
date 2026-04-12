from django.urls import path
from .views import dashboard_home, settings_view

urlpatterns = [
    path("dashboard/", dashboard_home, name="dashboard"),
    path("settings/", settings_view, name="settings"),
]