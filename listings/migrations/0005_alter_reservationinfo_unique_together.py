# Generated by Django 3.2 on 2021-09-04 01:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0004_alter_reservationinfo_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reservationinfo',
            unique_together={('reserved_date', 'hotel_room')},
        ),
    ]
