# Generated by Django 4.2.3 on 2024-04-22 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CabApp', '0012_tsc_form_extra_hour_charge_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tripridehours',
            name='hours',
            field=models.CharField(blank=True, default=0.0, max_length=20, null=True),
        ),
    ]
