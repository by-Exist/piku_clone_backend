# Generated by Django 3.1.5 on 2021-01-13 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worldcupapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worldcup',
            name='media_type',
        ),
        migrations.AddField(
            model_name='album',
            name='media_type',
            field=models.CharField(choices=[('T', 'text'), ('I', 'image'), ('G', 'gif'), ('V', 'video')], default='T', max_length=1, verbose_name='데이터 타입'),
            preserve_default=False,
        ),
    ]
