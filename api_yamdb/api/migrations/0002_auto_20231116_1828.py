# Generated by Django 3.2 on 2023-11-16 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Название')),
                ('slug', models.SlugField(verbose_name='Slug Категории')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Название')),
                ('slug', models.SlugField(verbose_name='Slug Жанра')),
            ],
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ('year',)},
        ),
        migrations.RemoveField(
            model_name='title',
            name='pub_date',
        ),
        migrations.RemoveField(
            model_name='title',
            name='title',
        ),
        migrations.AddField(
            model_name='title',
            name='description',
            field=models.TextField(default=1, verbose_name='Описание'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='title',
            name='name',
            field=models.TextField(default=1, verbose_name='Название'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='title',
            name='year',
            field=models.DateTimeField(auto_now_add=True, default=1, verbose_name='Год выпуска'),
            preserve_default=False,
        ),
    ]
