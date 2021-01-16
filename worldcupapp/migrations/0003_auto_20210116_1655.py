# Generated by Django 3.1.5 on 2021-01-16 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worldcupapp', '0002_auto_20210116_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='media_type',
            field=models.CharField(choices=[('T', 'text'), ('I', 'image'), ('G', 'gif'), ('V', 'video')], max_length=1, verbose_name='데이터 타입'),
        ),
        migrations.AlterField(
            model_name='album',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to='worldcupapp/album/thumbnail/%Y/%m/%d/', verbose_name='썸네일'),
        ),
    ]