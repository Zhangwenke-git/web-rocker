# Generated by Django 3.2 on 2021-09-09 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0002_rename_photo_userprofile_upload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='steplog',
            name='detail',
            field=models.JSONField(verbose_name='操作详情'),
        ),
        migrations.AlterField(
            model_name='steplog',
            name='origin',
            field=models.JSONField(null=True, verbose_name='原始数据'),
        ),
    ]