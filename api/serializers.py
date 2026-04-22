from rest_framework import serializers
from dashboard.models import Lesson  # adjust mo if iba name

class LessonSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.username', read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'category', 'description', 'status', 'price_coins', 'created_at', 'teacher', 'teacher_name']