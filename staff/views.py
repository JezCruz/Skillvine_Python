from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import staff_required
from .models import Report
from dashboard.models import Wallet, CoinTransaction

User = get_user_model()


@login_required
@staff_required
def staff_dashboard(request):
    total_users = User.objects.count()
    total_students = User.objects.filter(role="student").count()
    total_teachers = User.objects.filter(role="teacher").count()
    total_staff = User.objects.filter(is_staff=True).count()

    total_sales = 0
    total_coins = Wallet.objects.aggregate(total=Sum("balance"))["total"] or 0
    open_reports = Report.objects.filter(status="pending").count()
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
        "user_growth_labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "user_growth_data": [2, 4, 6, 7, 10, 12, 15],
        "sales_labels": ["Jan", "Feb", "Mar", "Apr"],
        "sales_data": [0, 0, 0, 0],
        "coins_labels": ["Earned", "Spent", "Held"],
        "coins_data": [0, 0, total_coins],
    }
    return render(request, "staff/dashboard.html", context)


@login_required
@staff_required
def staff_coins(request):
    wallets = Wallet.objects.select_related("user").order_by("-balance", "user__username")
    transactions = CoinTransaction.objects.all().order_by("-created_at")[:20]

    total_coins = wallets.aggregate(total=Sum("balance"))["total"] or 0

    context = {
        "wallets": wallets,
        "transactions": transactions,
        "total_coins": total_coins,
    }
    return render(request, "staff/coins.html", context)


@login_required
@staff_required
def adjust_user_coins(request, user_id):
    if request.method != "POST":
        return redirect("staff_coins")

    user = get_object_or_404(User, id=user_id)
    wallet, _ = Wallet.objects.get_or_create(user=user)

    action = request.POST.get("action", "").strip()
    amount_raw = request.POST.get("amount", "").strip()
    note = request.POST.get("note", "").strip()

    if not amount_raw.isdigit():
        messages.error(request, "Amount must be a valid whole number.")
        return redirect("staff_coins")

    amount = int(amount_raw)

    if amount <= 0:
        messages.error(request, "Amount must be greater than zero.")
        return redirect("staff_coins")

    if action == "credit":
        wallet.balance += amount
        wallet.save()

        CoinTransaction.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type="credit",
            note=note,
            created_by=request.user,
        )

        messages.success(request, f"Added {amount} coins to {user.username}.")

    elif action == "debit":
        if wallet.balance < amount:
            messages.error(request, f"{user.username} does not have enough coins.")
            return redirect("staff_coins")

        wallet.balance -= amount
        wallet.save()

        CoinTransaction.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type="debit",
            note=note,
            created_by=request.user,
        )

        messages.success(request, f"Removed {amount} coins from {user.username}.")
    else:
        messages.error(request, "Invalid action.")

    return redirect("staff_coins")


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
        messages.error(request, "You cannot change your own staff status.")
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
        messages.error(request, "You cannot remove your own staff access.")
        return redirect("staff_users")

    user.is_staff = False
    user.save()

    messages.success(request, f"{user.username} removed from staff.")
    return redirect("staff_users")



@login_required
@staff_required
def deactivate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.user.id == user.id:
        messages.error(request, "You cannot deactivate yourself.")
        return redirect("staff_users")

    user.is_active = False
    user.save()

    messages.success(request, f"{user.username} has been deactivated.")
    return redirect("staff_users")


@login_required
@staff_required
def reactivate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    user.is_active = True
    user.save()

    messages.success(request, f"{user.username} has been reactivated.")
    return redirect("staff_users")


@login_required
@staff_required
def staff_reports(request):
    reports = Report.objects.select_related("reporter", "reported_user").order_by("-created_at")

    context = {
        "reports": reports,
    }

    return render(request, "staff/reports.html", context)


@login_required
@staff_required
def resolve_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    report.status = "resolved"
    report.save()

    messages.success(request, "Report marked as resolved.")
    return redirect("staff_reports")