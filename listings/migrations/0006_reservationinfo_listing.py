# Generated by Django 3.2 on 2021-09-08 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0005_alter_reservationinfo_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservationinfo',
            name='listing',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservation_info', to='listings.listing'),
        ),
    ]
