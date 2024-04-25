from django.urls import path

from materials.apps import CoursesConfig
from rest_framework.routers import DefaultRouter
from materials.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentListAPIView, PaymentCreateAPIView

app_name = CoursesConfig.name

router = DefaultRouter()
router.register(r'materials', CourseViewSet, basename='materials')

urlpatterns = [
    path('lesson/create', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
    # payment
    path('payment/', PaymentListAPIView.as_view(), name='payment-list'),
    path('payment/create', PaymentCreateAPIView.as_view(), name='payment-create'),
] + router.urls