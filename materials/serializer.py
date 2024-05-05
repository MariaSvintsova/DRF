from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from materials.validators import TitleValodator, YouTubeLinkValidator
from materials.models import Course, Lesson
from users.models import User, Payment, Subscription


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            TitleValodator(field='title'),
            serializers.UniqueTogetherValidator(fields=['title', 'description'], queryset=Lesson.objects.all()),
            YouTubeLinkValidator(field='video_link')
        ]


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    total_lessons = serializers.SerializerMethodField(read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_total_lessons(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, object):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user, course=object).exists()

class PaymentSerializer(serializers.ModelSerializer):
    course = SlugRelatedField(slug_field='title', queryset=Course.objects.all())
    lesson = SlugRelatedField(slug_field='title', queryset=Lesson.objects.all())
    user = SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Payment
        fields = '__all__'

class PaymentCreateSerializers(serializers.ModelSerializer):
    payment = PaymentSerializer(many=True)

    class Meta:
        model = Payment
        fields = '__all__'

    def create(self, validated_data):
        payment = validated_data.pop('payment')

        payment_item = Payment.objects.crete(**validated_data)

        for m in payment_item:
            Payment.objects.crete(**m, payment=payment_item)
        return payment_item
