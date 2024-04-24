from django.db import models

NULLABLE = {'blank': True, 'null': True}

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    photo = models.ImageField(upload_to='items', **NULLABLE, verbose_name='Фото')
    description = models.TextField(verbose_name='Oписание')

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


    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
