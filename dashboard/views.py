from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect


@login_required
def dashboard_home(request):
    if request.user.role == "teacher":
        template_name = "dashboard/teacher_dashboard.html"
        context = {
            "user": request.user,
            "total_students": 12,
            "active_lessons": 5,
            "average_rating": 4.8,
            "recent_activities": [
                "A new student enrolled in your guitar class.",
                "You received a 5-star rating from a student.",
                "Your piano lesson schedule was updated.",
            ],
        }
    else:
        template_name = "dashboard/student_dashboard.html"
        context = {
            "user": request.user,
            "enrolled_classes": 3,
            "coins": 120,
            "unread_notifications": 4,
            "recent_activities": [
                "Your English lesson starts tomorrow.",
                "A teacher replied to your session request.",
                "You earned 20 coins from an activity bonus.",
            ],
        }

    return render(request, template_name, context)


@login_required
def settings_view(request):
    return render(request, "dashboard/settings.html", {"user": request.user})


@login_required
def profile_view(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()

        if full_name:
            request.user.full_name = full_name
            request.user.first_name = full_name.split()[0] if full_name else ""
            request.user.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
        else:
            messages.error(request, "Full name cannot be empty.")

    return render(request, "dashboard/profile.html", {
        "user": request.user,
    })


@login_required
def my_learning_view(request):
    return render(request, "dashboard/my_learning.html", {"user": request.user})


@login_required
def notifications_view(request):
    return render(request, "dashboard/notifications.html", {"user": request.user})


@login_required
def my_students_view(request):
    return render(request, "dashboard/my_students.html", {"user": request.user})


@login_required
def lessons_view(request):
    return render(request, "dashboard/lessons.html", {"user": request.user})