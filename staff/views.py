from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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


def staff_users(request):
    query = request.GET.get("q", "")
    role = request.GET.get("role", "")

    users = User.objects.all()

    if query:
        users = users.filter(username__icontains=query)

    if role:
        users = users.filter(role=role)

    context = {
        "users": users,
        "query": query,
        "role": role,
    }

    return render(request, "staff/users.html", context)