# Generated by Django 4.2.3 on 2024-03-14 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CabApp', '0004_tsc_form_bill_qr'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer_Feedbacks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=150, null=True)),
                ('feedback', models.TextField()),
            ],
        ),
    ]
