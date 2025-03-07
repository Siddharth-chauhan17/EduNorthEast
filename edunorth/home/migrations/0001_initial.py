# Generated by Django 5.1.6 on 2025-03-05 19:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subtopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource_type', models.CharField(choices=[('youtube', 'YouTube Video'), ('blog', 'Blog Article')], max_length=10)),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('subtopic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources', to='home.subtopic')),
            ],
        ),
        migrations.CreateModel(
            name='UserSearchHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='subtopic',
            name='search',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subtopics', to='home.usersearchhistory'),
        ),
    ]
