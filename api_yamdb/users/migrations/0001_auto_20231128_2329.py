# Generated by Django 3.2.20 on 2023-11-28 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', 'initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.UUIDField(blank=True, null=True, verbose_name='Код'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Имя.'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Фамилия.'),
        ),
    ]