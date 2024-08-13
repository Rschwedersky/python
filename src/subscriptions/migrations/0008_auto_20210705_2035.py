# Generated by Django 3.1.1 on 2021-07-05 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0007_profile_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='department',
        ),
        migrations.AddField(
            model_name='plan',
            name='with_dashboard',
            field=models.BooleanField(default=False),
        ),
    ]
