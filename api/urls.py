from django.urls import path
from .views import (
    get_lessons,
    get_lesson,
    create_lesson,
    update_lesson,
    delete_lesson,
    register_user,
    profile,
    my_lessons,
    create_booking,
    my_bookings,
    teacher_bookings,
    update_booking_status,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('lessons/', get_lessons),
    path('lessons/create/', create_lesson),
    path('lessons/<int:id>/', get_lesson),
    path('lessons/<int:id>/update/', update_lesson),
    path('lessons/<int:id>/delete/', delete_lesson),
    
    path('my-lessons/', my_lessons),
    path('bookings/create/', create_booking),
    path('my-bookings/', my_bookings),
    path('teacher-bookings/', teacher_bookings),
    path('booking/<int:id>/update/', update_booking_status),

    path('register/', register_user),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', profile),
]