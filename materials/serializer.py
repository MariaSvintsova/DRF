from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from materials.models import Course, Lesson
from users.models import User, Payment


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    total_lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, obj):
        return obj.lesson_set.count()

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


