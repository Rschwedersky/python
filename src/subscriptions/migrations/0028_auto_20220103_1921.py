# Generated by Django 3.2.10 on 2022-01-03 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0027_sessioninfo_user_ip_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='created_at',
        ),
        migrations.AddField(
            model_name='subscription',
            name='extra_queries',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subscription',
            name='number_of_hired_services',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='subscription',
            name='payment_period',
            field=models.CharField(choices=[('MONTHLY', 'Monthly'), ('YEARLY', 'Yearly')], default='MONTHLY', max_length=10),
        ),
        migrations.AddField(
            model_name='subscription',
            name='queries_limit',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subscription',
            name='with_dashboard',
            field=models.BooleanField(default=False),
        ),
    ]
