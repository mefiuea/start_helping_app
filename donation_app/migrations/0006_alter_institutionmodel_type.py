# Generated by Django 4.0.4 on 2022-05-20 08:37

from django.db import migrations, models
import donation_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('donation_app', '0005_alter_donationmodel_pick_up_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institutionmodel',
            name='type',
            field=models.CharField(choices=[('Fundacja', 'F'), ('Organizacja Pozarządowa', 'OP'), ('Zbiórka Lokalna', 'ZL')], default=donation_app.models.Type['F'], max_length=23, verbose_name='Typ'),
        ),
    ]
