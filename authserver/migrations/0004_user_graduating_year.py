# Generated by Django 4.2.5 on 2023-12-12 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authserver', '0003_user_email_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='graduating_year',
            field=models.IntegerField(default=2030),
        ),
    ]
