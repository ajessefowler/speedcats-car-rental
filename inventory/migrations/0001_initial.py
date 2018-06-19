# Generated by Django 2.0.6 on 2018-06-19 00:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pick_up_time', models.DateTimeField()),
                ('drop_off_time', models.DateTimeField()),
                ('miles_driven', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('ID', models.IntegerField(primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=2)),
                ('zipcode', models.IntegerField()),
                ('phone', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('VIN', models.CharField(max_length=17)),
                ('year', models.IntegerField()),
                ('make', models.CharField(max_length=30)),
                ('model', models.CharField(max_length=30)),
                ('color', models.CharField(max_length=10)),
                ('mileage', models.IntegerField()),
                ('image', models.ImageField(blank=True, upload_to='vehicle_photos')),
                ('description', models.CharField(default='', max_length=800)),
                ('status', models.CharField(choices=[('m', 'Maintenance'), ('l', 'Loaned'), ('a', 'Available'), ('r', 'Reserved')], default='a', max_length=1)),
                ('vehicle_type', models.CharField(choices=[('c', 'Car'), ('s', 'SUV'), ('t', 'Truck')], default='c', max_length=1)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Store')),
            ],
        ),
        migrations.AddField(
            model_name='reservation',
            name='drop_off_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='drop_off_store', to='inventory.Store'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='pick_up_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pick_up_store', to='inventory.Store'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reservation',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Vehicle'),
        ),
    ]