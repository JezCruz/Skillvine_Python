import json

from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout
from django.shortcuts import redirect


User = get_user_model()


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == "GET":
        return render(request, "users/login.html")

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON."}, status=400)

    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    if not email or not password:
        return JsonResponse({"error": "Email and password are required."}, status=400)

    try:
        user_obj = User.objects.get(email=email)
        username = user_obj.username
    except User.DoesNotExist:
        return JsonResponse({"error": "Invalid email or password."}, status=400)

    user = authenticate(request, username=username, password=password)

    if user is None:
        return JsonResponse({"error": "Invalid email or password."}, status=400)

    login(request, user)

    return JsonResponse({
        "message": "Login successful.",
        "redirect": "/dashboard/",
    }, status=200)


@require_http_methods(["GET", "POST"])
def signup_view(request):
    if request.method == "GET":
        return render(request, "users/signup.html")

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON."}, status=400)

    full_name = data.get("full_name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()
    role = data.get("role", "").strip().lower()

    if not full_name or not email or not password or not role:
        return JsonResponse({"error": "Please fill all fields."}, status=400)

    if role not in ["student", "teacher"]:
        return JsonResponse({"error": "Invalid role selected."}, status=400)

    if User.objects.filter(email=email).exists():
        return JsonResponse({"error": "Email is already registered."}, status=400)

    user = User.objects.create_user(
        username=email,
        email=email,
        password=password,
        full_name=full_name,
        first_name=full_name.split()[0] if full_name else "",
        role=role,
    )

    return JsonResponse({
        "message": "Signup successful.",
        "redirect": "/dashboard/",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
        }
    }, status=201)


def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("login")