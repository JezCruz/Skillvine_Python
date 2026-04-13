from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.action(description="Mark selected users as students")
def make_student(modeladmin, request, queryset):
    queryset.update(role="student")


@admin.action(description="Mark selected users as teachers")
def make_teacher(modeladmin, request, queryset):
    queryset.update(role="teacher")


@admin.action(description="Activate selected users")
def activate_users(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description="Deactivate selected users")
def deactivate_users(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        "id",
        "username",
        "email",
        "full_name",
        "role",
        "is_staff",
        "is_active",
    )
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email", "full_name")
    ordering = ("id",)
    actions = [make_student, make_teacher, activate_users, deactivate_users]

    fieldsets = UserAdmin.fieldsets + (
        ("Skillvine Info", {"fields": ("full_name", "role")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Skillvine Info", {"fields": ("full_name", "role")}),
    )