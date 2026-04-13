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
    if request.user.role == "teacher":
        template_name = "dashboard/teacher_notifications.html"
        notifications = [
            {
                "title": "New Student Enrollment",
                "message": "A new student joined your Beginner Guitar class.",
                "time": "2 hours ago",
                "status": "unread",
            },
            {
                "title": "Lesson Reminder",
                "message": "You have a scheduled piano lesson tomorrow at 3:00 PM.",
                "time": "5 hours ago",
                "status": "read",
            },
            {
                "title": "New Rating Received",
                "message": "You received a 5-star rating from one of your students.",
                "time": "1 day ago",
                "status": "read",
            },
        ]
    else:
        template_name = "dashboard/student_notifications.html"
        notifications = [
            {
                "title": "Upcoming Lesson",
                "message": "Your English speaking lesson starts tomorrow at 10:00 AM.",
                "time": "1 hour ago",
                "status": "unread",
            },
            {
                "title": "Teacher Response",
                "message": "Your teacher replied to your session request.",
                "time": "4 hours ago",
                "status": "read",
            },
            {
                "title": "Coins Added",
                "message": "You received 20 bonus coins for completing an activity.",
                "time": "1 day ago",
                "status": "read",
            },
        ]

    return render(request, template_name, {
        "user": request.user,
        "notifications": notifications,
    })


@login_required
def my_students_view(request):
    return render(request, "dashboard/my_students.html", {"user": request.user})


@login_required
def lessons_view(request):
    return render(request, "dashboard/lessons.html", {"user": request.user})