# Generated by Django 4.0.4 on 2022-05-31 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation_app', '0002_donationmodel_date_add_donationmodel_is_taken'),
    ]

    operations = [
        migrations.AddField(
            model_name='donationmodel',
            name='is_taken_date',
            field=models.DateTimeField(null=True),
        ),
    ]
