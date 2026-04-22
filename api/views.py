from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from dashboard.models import Lesson
from .serializers import LessonSerializer, RegisterSerializer

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            "message": "User registered successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_lesson(request, id):
    lesson = get_object_or_404(Lesson, id=id)
    serializer = LessonSerializer(lesson)
    return Response(serializer.data)

@api_view(['GET'])
def get_lessons(request):
    lessons = Lesson.objects.filter(status='active')
    serializer = LessonSerializer(lessons, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_lesson(request):
    serializer = LessonSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(teacher=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_lesson(request, id):
    lesson = get_object_or_404(Lesson, id=id)

    if lesson.teacher != request.user:
        return Response({"error": "Not allowed"}, status=403)

    serializer = LessonSerializer(lesson, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_lesson(request, id):
    lesson = get_object_or_404(Lesson, id=id)

    if lesson.teacher != request.user:
        return Response({"error": "Not allowed"}, status=403)

    lesson.delete()
    return Response({"message": "Deleted"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_lessons(request):
    lessons = Lesson.objects.filter(teacher=request.user)
    serializer = LessonSerializer(lessons, many=True)
    return Response(serializer.data)