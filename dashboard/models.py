from django.conf import settings
from django.db import models


class Lesson(models.Model):
    STATUS_CHOICES = (
        ("active", "Active"),
        ("draft", "Draft"),
    )

    CATEGORY_CHOICES = (
        ("music", "Music"),
        ("language", "Language"),
        ("fitness", "Fitness"),
        ("academics", "Academics"),
        ("other", "Other"),
    )

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lessons"
    )
    title = models.CharField(max_length=150)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="other")
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    
class Enrollment(models.Model):
    STATUS_CHOICES = (
        ("enrolled", "Enrolled"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="enrolled")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "lesson")

    def __str__(self):
        return f"{self.student} -> {self.lesson}"
    

class Enrollment(models.Model):
    STATUS_CHOICES = (
        ("enrolled", "Enrolled"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="enrolled")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "lesson")

    def __str__(self):
        return f"{self.student} -> {self.lesson}"