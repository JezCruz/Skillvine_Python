from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from dashboard.models import Lesson, Booking, Wallet, CoinTransaction, Enrollment
from .serializers import LessonSerializer, RegisterSerializer, BookingSerializer, EmailOrUsernameTokenObtainPairSerializer


User = get_user_model()

class EmailOrUsernameLoginView(TokenObtainPairView):
    serializer_class = EmailOrUsernameTokenObtainPairSerializer
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    wallet = getattr(user, "wallet", None)

    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "coins": wallet.balance if wallet else 0,
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
                "role": user.role,
            }
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_lessons(request):
    lessons = Lesson.objects.filter(status='active').order_by('-created_at')
    serializer = LessonSerializer(lessons, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_lesson(request, id):
    lesson = get_object_or_404(Lesson, id=id)
    serializer = LessonSerializer(lesson)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_lesson(request):
    if request.user.role != 'teacher':
        return Response({"error": "Only teachers can create lessons"}, status=status.HTTP_403_FORBIDDEN)

    serializer = LessonSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(teacher=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_lesson(request, id):
    lesson = get_object_or_404(Lesson, id=id)

    if lesson.teacher != request.user:
        return Response({"error": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

    serializer = LessonSerializer(lesson, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_lesson(request, id):
    lesson = get_object_or_404(Lesson, id=id)

    if lesson.teacher != request.user:
        return Response({"error": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

    lesson.delete()
    return Response({"message": "Lesson deleted successfully"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_lessons(request):
    if request.user.role != 'teacher':
        return Response({"error": "Only teachers can view their lessons"}, status=status.HTTP_403_FORBIDDEN)

    lessons = Lesson.objects.filter(teacher=request.user).order_by('-created_at')
    serializer = LessonSerializer(lessons, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_booking(request):
    if request.user.role != 'student':
        return Response({"error": "Only students can book lessons"}, status=status.HTTP_403_FORBIDDEN)

    lesson_id = request.data.get('lesson')

    if not lesson_id:
        return Response({"error": "Lesson ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    lesson = get_object_or_404(Lesson, id=lesson_id)

    if lesson.teacher == request.user:
        return Response({"error": "You cannot book your own lesson"}, status=status.HTTP_400_BAD_REQUEST)

    if Booking.objects.filter(student=request.user, lesson=lesson).exists():
        return Response({"error": "You already booked this lesson"}, status=status.HTTP_400_BAD_REQUEST)

    booking = Booking.objects.create(
        student=request.user,
        lesson=lesson,
        status='pending'
    )

    serializer = BookingSerializer(booking)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_bookings(request):
    if request.user.role != 'student':
        return Response({"error": "Only students can view their bookings"}, status=status.HTTP_403_FORBIDDEN)

    bookings = Booking.objects.filter(student=request.user).order_by('-created_at')
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def teacher_bookings(request):
    if request.user.role != 'teacher':
        return Response({"error": "Only teachers can view booking requests"}, status=status.HTTP_403_FORBIDDEN)

    bookings = Booking.objects.filter(lesson__teacher=request.user).order_by('-created_at')
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_booking_status(request, id):
    if request.user.role != 'teacher':
        return Response({"error": "Only teachers can update booking status"}, status=status.HTTP_403_FORBIDDEN)

    booking = get_object_or_404(Booking, id=id)

    if booking.lesson.teacher != request.user:
        return Response({"error": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

    if booking.status != 'pending':
        return Response({"error": "This booking is already processed"}, status=status.HTTP_400_BAD_REQUEST)

    status_value = request.data.get('status')

    if status_value not in ['approved', 'declined']:
        return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

    if status_value == 'approved':
        student_wallet = get_object_or_404(Wallet, user=booking.student)
        teacher_wallet = get_object_or_404(Wallet, user=booking.lesson.teacher)

        price = booking.lesson.price_coins

        if student_wallet.balance < price:
            return Response({"error": "Student has insufficient coins"}, status=status.HTTP_400_BAD_REQUEST)

        student_wallet.balance -= price
        student_wallet.save()

        teacher_wallet.balance += price
        teacher_wallet.save()

        CoinTransaction.objects.create(
            user=booking.student,
            transaction_type='debit',
            amount=price,
            description=f"Booked lesson: {booking.lesson.title}"
        )

        CoinTransaction.objects.create(
            user=booking.lesson.teacher,
            transaction_type='credit',
            amount=price,
            description=f"Payment received for lesson: {booking.lesson.title}"
        )

        Enrollment.objects.get_or_create(
            student=booking.student,
            lesson=booking.lesson,
            defaults={"status": "enrolled"}
        )

    booking.status = status_value
    booking.save()

    return Response({
        "message": f"Booking {status_value} successfully",
        "status": booking.status,
    })



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_enrollments(request):
    if request.user.role != 'student':
        return Response({"error": "Only students can view enrollments"}, status=status.HTTP_403_FORBIDDEN)

    enrollments = Enrollment.objects.filter(student=request.user).order_by('-created_at')

    data = []
    for enrollment in enrollments:
        data.append({
            "id": enrollment.id,
            "lesson_id": enrollment.lesson.id,
            "lesson_title": enrollment.lesson.title,
            "teacher_username": enrollment.lesson.teacher.username,
            "status": enrollment.status,
            "created_at": enrollment.created_at,
        })

    return Response(data)