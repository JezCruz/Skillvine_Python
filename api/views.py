from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dashboard.models import Lesson
from .serializers import LessonSerializer

@api_view(['GET'])
def get_lesson(request, id):
    lesson = get_object_or_404(Lesson, id=id)
    serializer = LessonSerializer(lesson)
    return Response(serializer.data)

@api_view(['GET'])
def get_lessons(request):
    lessons = Lesson.objects.all()
    serializer = LessonSerializer(lessons, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_lesson(request):
    serializer = LessonSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def update_lesson(request, id):
    lesson = get_object_or_404(Lesson, id=id)
    serializer = LessonSerializer(lesson, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_lesson(request, id):
    lesson = get_object_or_404(Lesson, id=id)
    lesson.delete()
    return Response({"message": "Lesson deleted"})