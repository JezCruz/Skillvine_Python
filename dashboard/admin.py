from django.contrib import admin
from .models import Lesson, Enrollment, Wallet, CoinTransaction

admin.site.site_header = "Skillvine Admin"
admin.site.site_title = "Skillvine Admin Portal"
admin.site.index_title = "Welcome to Skillvine Management"


@admin.action(description="Mark selected lessons as Active")
def make_active(modeladmin, request, queryset):
    queryset.update(status="active")


@admin.action(description="Mark selected lessons as Draft")
def make_draft(modeladmin, request, queryset):
    queryset.update(status="draft")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "teacher", "category", "status", "created_at")
    list_filter = ("category", "status", "created_at")
    search_fields = ("title", "teacher__email", "teacher__full_name")
    ordering = ("-created_at",)
    actions = [make_active, make_draft]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            kwargs["queryset"] = db_field.remote_field.model.objects.filter(role="teacher")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "lesson", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("student__email", "student__full_name", "lesson__title")
    ordering = ("-created_at",)


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "balance")
    search_fields = ("user__email", "user__full_name", "user__username")


@admin.register(CoinTransaction)
class CoinTransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "transaction_type", "amount", "description", "created_at")
    list_filter = ("transaction_type", "created_at")
    search_fields = ("user__email", "user__full_name", "description")
    ordering = ("-created_at",)