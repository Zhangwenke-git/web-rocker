# Generated by Django 3.2 on 2021-09-02 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='photo',
            new_name='upload',
        ),
    ]
