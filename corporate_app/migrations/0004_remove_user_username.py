# Generated by Django 4.1.5 on 2023-01-26 05:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corporate_app', '0003_alter_user_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
