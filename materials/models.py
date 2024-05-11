from django.db import models

from config import settings


NULLABLE = {'blank': True, 'null': True}

# Create your models here.
class Course(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name='Название')
    photo = models.ImageField(upload_to='items', **NULLABLE, verbose_name='Фото')
    description = models.TextField(verbose_name='Oписание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.IntegerField(default=1000, verbose_name='Цена')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    photo = models.ImageField(upload_to='items', **NULLABLE, verbose_name='Фото')
    description = models.TextField(verbose_name='Oписание')
    video_link = models.URLField(verbose_name='Ссылка')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='Курс')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


