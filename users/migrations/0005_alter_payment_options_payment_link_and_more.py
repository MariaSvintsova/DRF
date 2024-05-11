# Generated by Django 5.0.4 on 2024-05-09 19:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_subscription'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name': 'Оплата', 'verbose_name_plural': 'Оплаты'},
        ),
        migrations.AddField(
            model_name='payment',
            name='link',
            field=models.URLField(blank=True, help_text='Укажите ссылку на оплату', max_length=400, null=True, verbose_name='Ссылка на оплату'),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Cash'), ('bank_transfer', 'Bank Transfer')], default='bank_transfer', max_length=20),
        ),
        migrations.AddField(
            model_name='payment',
            name='session_id',
            field=models.CharField(blank=True, help_text='Укажите ID сессии', max_length=255, null=True, verbose_name='ID сессии'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма оплаты'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(blank=True, help_text='Укажите пользователя', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
