from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Lesson, Enrollment

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
def my_learning_view(request):
    if request.user.role != "student":
        messages.error(request, "Only students can access My Learning.")
        return redirect("dashboard")

    enrollments = Enrollment.objects.filter(student=request.user).select_related(
        "lesson", "lesson__teacher"
    ).order_by("-created_at")

    return render(request, "dashboard/my_learning.html", {
        "user": request.user,
        "enrollments": enrollments,
    })


@login_required
def lessons_view(request):
    if request.user.role != "teacher":
        messages.error(request, "Only teachers can access lessons management.")
        return redirect("dashboard")

    lesson_items = Lesson.objects.filter(teacher=request.user).order_by("-created_at")

    return render(request, "dashboard/lessons.html", {
        "user": request.user,
        "lesson_items": lesson_items,
    })


@login_required
def create_lesson_view(request):
    if request.user.role != "teacher":
        messages.error(request, "Only teachers can create lessons.")
        return redirect("dashboard")

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        category = request.POST.get("category", "").strip()
        description = request.POST.get("description", "").strip()
        status = request.POST.get("status", "").strip()

        if not title or not category or not status:
            messages.error(request, "Please fill in all required fields.")
            return redirect("create_lesson")

        Lesson.objects.create(
            teacher=request.user,
            title=title,
            category=category,
            description=description,
            status=status,
        )

        messages.success(request, "Lesson created successfully.")
        return redirect("lessons")

    return render(request, "dashboard/create_lesson.html", {
        "user": request.user,
    })


@login_required
def browse_lessons_view(request):
    if request.user.role != "student":
        messages.error(request, "Only students can browse lessons.")
        return redirect("dashboard")

    lessons = Lesson.objects.filter(status="active").select_related("teacher").order_by("-created_at")
    enrolled_lesson_ids = set(
        Enrollment.objects.filter(student=request.user).values_list("lesson_id", flat=True)
    )

    return render(request, "dashboard/browse_lessons.html", {
        "user": request.user,
        "lessons": lessons,
        "enrolled_lesson_ids": enrolled_lesson_ids,
    })


@login_required
def enroll_lesson_view(request, lesson_id):
    if request.user.role != "student":
        messages.error(request, "Only students can enroll in lessons.")
        return redirect("dashboard")

    if request.method != "POST":
        return redirect("browse_lessons")

    try:
        lesson = Lesson.objects.get(id=lesson_id, status="active")
    except Lesson.DoesNotExist:
        messages.error(request, "Lesson not found.")
        return redirect("browse_lessons")

    if lesson.teacher_id == request.user.id:
        messages.error(request, "You cannot enroll in your own lesson.")
        return redirect("browse_lessons")

    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        lesson=lesson,
        defaults={"status": "enrolled"},
    )

    if created:
        messages.success(request, f"You enrolled in '{lesson.title}' successfully.")
    else:
        messages.info(request, f"You are already enrolled in '{lesson.title}'.")

    return redirect("browse_lessons")   