from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard_home(request):
    if request.user.role == "teacher":
        template_name = "dashboard/teacher_dashboard.html"
    else:
        template_name = "dashboard/student_dashboard.html"

    return render(request, template_name, {
        "user": request.user,
    })

@login_required
def settings_view(request):
    return render(request, "dashboard/settings.html", {
        "user": request.user,
    })

@login_required
def profile_view(request):
    return render(request, "dashboard/profile.html", {
        "user": request.user,
    })