"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.http import FileResponse, Http404
from pathlib import Path
from django.conf import settings

def download_apk(request, filename):
    file_path = Path(settings.BASE_DIR) / "downloads" / "apk" / filename

    if not file_path.exists():
        raise Http404("APK not found")

    return FileResponse(
        open(file_path, "rb"),
        as_attachment=True,
        filename=filename
    )

urlpatterns = [
    path("admin/", admin.site.urls),

    path("downloads/apk/<str:filename>", download_apk),

    path("", include("core.urls")),
    path("", include("users.urls")),
    path("", include("dashboard.urls")),
    path("staff/", include("staff.urls")),
    path('api/', include('api.urls')),
]