from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from dashboard.models import Lesson, Booking
from .models import Notification

User = get_user_model()


class EmailOrUsernameTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'username'

    def validate(self, attrs):
        login = attrs.get("username")
        password = attrs.get("password")

        user_obj = User.objects.filter(email__iexact=login).first()

        if user_obj:
            attrs["username"] = user_obj.username

        return super().validate(attrs)
    

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
    teacher_username = serializers.CharField(source='lesson.teacher.username', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id',
            'student_id',
            'student_username',
            'lesson_id',
            'lesson_title',
            'lesson_price',
            'teacher_username',
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
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password', 'password2']
        read_only_fields = ['id']

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required.")

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already exists.")

        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
        )

        return user
    

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "title", "message", "is_read", "created_at"]