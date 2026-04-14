from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q

from .decorators import staff_required

User = get_user_model()


@login_required
@staff_required
def staff_dashboard(request):
    total_users = User.objects.count()
    total_students = User.objects.filter(role="student").count()
    total_teachers = User.objects.filter(role="teacher").count()
    total_staff = User.objects.filter(is_staff=True).count()

    # placeholder metrics for now
    total_sales = 0
    total_coins = 0
    open_reports = 0
    system_assets = 0

    context = {
        "total_users": total_users,
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_staff": total_staff,
        "total_sales": total_sales,
        "total_coins": total_coins,
        "open_reports": open_reports,
        "system_assets": system_assets,

        # chart demo data
        "user_growth_labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "user_growth_data": [2, 4, 6, 7, 10, 12, 15],

        "sales_labels": ["Jan", "Feb", "Mar", "Apr"],
        "sales_data": [0, 0, 0, 0],

        "coins_labels": ["Earned", "Spent", "Held"],
        "coins_data": [0, 0, 0],
    }
    return render(request, "staff/dashboard.html", context)


@login_required
@staff_required
def staff_users(request):
    query = request.GET.get("q", "").strip()
    role = request.GET.get("role", "").strip()
    status = request.GET.get("status", "").strip()

    users = User.objects.all().order_by("-date_joined")

    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query)
        )

    if role:
        users = users.filter(role=role)

    if status == "active":
        users = users.filter(is_active=True)
    elif status == "inactive":
        users = users.filter(is_active=False)

    context = {
        "users": users,
        "query": query,
        "role": role,
        "status": status,
    }

    return render(request, "staff/users.html", context)


@login_required
@staff_required
def make_user_staff(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.user.id == user.id:
        messages.error(request, "You cannot change your own staff status here.")
        return redirect("staff_users")

    user.is_staff = True
    user.save()

    messages.success(request, f"{user.username} is now a staff member.")
    return redirect("staff_users")


@login_required
@staff_required
def remove_user_staff(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.user.id == user.id:
        messages.error(request, "You cannot remove your own staff access here.")
        return redirect("staff_users")

    user.is_staff = False
    user.save()

    messages.success(request, f"{user.username} was removed from staff.")
    return redirect("staff_users")


@login_required
@staff_required
def deactivate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.user.id == user.id:
        messages.error(request, "You cannot deactivate your own account here.")
        return redirect("staff_users")

    user.is_active = False
    user.save()

    messages.success(request, f"{user.username} has been deactivated.")
    return redirect("staff_users")


@login_required
@staff_required
def reactivate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.user.id == user.id:
        messages.error(request, "You cannot reactivate your own account here.")
        return redirect("staff_users")

    user.is_active = True
    user.save()

    messages.success(request, f"{user.username} has been reactivated.")
    return redirect("staff_users")