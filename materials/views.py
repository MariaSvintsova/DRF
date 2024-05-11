from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django_filters.rest_framework import filters, DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics
from rest_framework.decorators import permission_classes
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from materials.models import Course, Lesson
from materials.paginators import MaterialsPagination
from materials.permissions import IsOwnerOrStaff
from materials.serializer import CourseSerializer, LessonSerializer, PaymentSerializer
from users.models import Payment, Subscription
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from materials.tasks import send_course_update_email

@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="description from swagger_auto_schema via method_decorator"
))
class CourseViewSet(viewsets.ModelViewSet):
    """ Viewset for courses """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = MaterialsPagination

@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description="description from swagger_auto_schema via method_decorator"
))
class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(self.queryset, pk=pk)

    def update_course(request, course_id):
        course = Course.objects.get(pk=course_id)
        subscribers = course.subscribers.all()
        for subscriber in subscribers:
            send_course_update_email.delay(subscriber.email)


class CourseCreateAPIView(generics.CreateAPIView):
    """ Course create edpoint """
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer

@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="description from swagger_auto_schema via method_decorator"
))
class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = MaterialsPagination

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrStaff]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()

class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('lesson', 'course', 'payment_method')
    ordering_fields = ('payment_date',)

class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer

@permission_classes([IsAuthenticated])
class SubscriptionAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        sub_item = Subscription.objects.filter(user=user, course=course)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if sub_item.exist():
            sub_item.delete()
            message = 'подписка удалена'
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'подписка добавлена'

        # Возвращаем ответ в API
        return Response({"message": message})


