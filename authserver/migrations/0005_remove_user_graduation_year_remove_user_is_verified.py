# Generated by Django 4.2.5 on 2023-11-13 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authserver', '0004_delete_authorizationcode_remove_user_access_token_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='graduation_year',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_verified',
        ),
    ]
