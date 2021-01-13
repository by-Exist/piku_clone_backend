# Generated by Django 3.1.5 on 2021-01-13 09:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import worldcupapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Worldcup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=127, verbose_name='제목')),
                ('intro', models.CharField(max_length=255, verbose_name='소개')),
                ('media_type', models.CharField(choices=[('T', 'text'), ('I', 'image'), ('G', 'gif'), ('V', 'video')], max_length=1, verbose_name='데이터 타입')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('play_count', models.PositiveIntegerField(default=0, verbose_name='플레이 횟수')),
                ('album', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='model', to='worldcupapp.album', verbose_name='앨범')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media', models.CharField(max_length=511, verbose_name='외부 비디오 링크')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_set', to='worldcupapp.album')),
            ],
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media', models.CharField(max_length=511, verbose_name='텍스트')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_set', to='worldcupapp.album')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media', models.FileField(upload_to=worldcupapp.models.get_upload_path, verbose_name='이미지 파일')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_set', to='worldcupapp.album')),
            ],
        ),
        migrations.CreateModel(
            name='Gif',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media', models.FileField(upload_to=worldcupapp.models.get_upload_path, verbose_name='움짤 파일 (gif -> mp4)')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gif_set', to='worldcupapp.album')),
            ],
        ),
    ]
