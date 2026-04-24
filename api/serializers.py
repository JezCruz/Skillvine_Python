from rest_framework import serializers
from django.contrib.auth import get_user_model

from dashboard.models import Lesson, Booking


User = get_user_model()


class LessonSerializer(serializers.ModelSerializer):
    teacher_id = serializers.IntegerField(source='teacher.id', read_only=True)
    teacher_username = serializers.CharField(source='teacher.username', read_only=True)

    class Meta:
        model = Lesson
        fields = [
            'id',
            'teacher_id',
            'teacher_username',
            'title',
            'category',
            'description',
            'status',
            'price_coins',
            'created_at',
        ]
        read_only_fields = ['id', 'teacher_id', 'teacher_username', 'created_at']


class BookingSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField(source='student.id', read_only=True)
    student_username = serializers.CharField(source='student.username', read_only=True)

    lesson_id = serializers.IntegerField(source='lesson.id', read_only=True)
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)
    lesson_price = serializers.IntegerField(source='lesson.price_coins', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id',
            'student_id',
            'student_username',
            'lesson',
            'lesson_id',
            'lesson_title',
            'lesson_price',
            'status',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'student_id',
            'student_username',
            'lesson_id',
            'lesson_title',
            'lesson_price',
            'status',
            'created_at',
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, default='student')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password', 'password2']
        read_only_fields = ['id']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=validated_data.get('role', 'student'),
        )

        return user