from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Report(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports_made")
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports_received")
    reason = models.TextField()

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("resolved", "Resolved"),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reporter} -> {self.reported_user} ({self.status})"