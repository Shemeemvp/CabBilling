# Generated by Django 4.2.3 on 2024-03-09 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CabApp', '0002_tsc_form'),
    ]

    operations = [
        migrations.AddField(
            model_name='tsc_form',
            name='destination',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
