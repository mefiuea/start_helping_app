# Generated by Django 4.0.4 on 2022-05-30 11:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('donation_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='donationmodel',
            name='date_add',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='donationmodel',
            name='is_taken',
            field=models.BooleanField(default=False, verbose_name='Odebrane?'),
        ),
    ]