from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes

from materials.models import Course
from users.models import Subscription
from users.serializer import MyTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    content = {'message': 'Это защищенное представление. Только авторизованные пользователи могут его видеть.'}
    return Response(content)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_object(request):
    if request.method == 'POST':
        return Response({'message': 'Объект успешно создан!'})
    else:
        return Response({'error': 'Метод не поддерживается'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class SubscriptionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        sub_item = Subscription.objects.filter(user=user, course=course)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if sub_item.exists():
            sub_item.delete()
            message = 'подписка удалена'
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'подписка добавлена'

        # Возвращаем ответ в API
        return Response({"message": message})


