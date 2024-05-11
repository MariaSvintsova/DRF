from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson

NULLABLE = {'blank': True, 'null': True}

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    phone_number = models.CharField(max_length=15, verbose_name='Телефон',  **NULLABLE)
    city = models.CharField(max_length=100, verbose_name='Город', default='Moscow')
    avatar = models.ImageField(upload_to='avatars/',  **NULLABLE, verbose_name='Аватарка')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number', 'city']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payment(models.Model):
    payment_date = models.DateField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    payment_method =  models.CharField(max_length=20, null=False, choices=[
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
    ],
    default='bank_transfer')
    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='ID сессии',
        help_text='Укажите ID сессии'
    )
    link = models.URLField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name='Ссылка на оплату',
        help_text='Укажите ссылку на оплату'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Пользователь',
        help_text='Укажите пользователя'
    )
    def __str__(self):
        return f'{self.user.username} - {self.payment_date}'

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'course']
