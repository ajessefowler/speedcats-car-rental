# Generated by Django 2.0.6 on 2018-06-10 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20180608_2224'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='status',
            field=models.CharField(choices=[('m', 'Maintenance'), ('l', 'Loaned'), ('a', 'Available'), ('r', 'Reserved')], default='a', max_length=1),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='vehicle_type',
            field=models.CharField(choices=[('c', 'Car'), ('s', 'SUV'), ('t', 'Truck')], default='c', max_length=1),
        ),
    ]
