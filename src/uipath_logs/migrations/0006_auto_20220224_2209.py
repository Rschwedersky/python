# Generated by Django 3.2.10 on 2022-02-24 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uipath_logs', '0005_merge_20220209_1714'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='processos',
            options={'verbose_name': 'Processos', 'verbose_name_plural': 'Processos'},
        ),
        migrations.AlterField(
            model_name='processos',
            name='average_single_transaction_time',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
