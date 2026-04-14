from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .decorators import staff_required

User = get_user_model()

@login_required
@staff_required
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