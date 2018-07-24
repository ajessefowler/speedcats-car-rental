# Generated by Django 2.0.6 on 2018-07-24 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicle',
            name='description',
        ),
        migrations.AddField(
            model_name='vehicle',
            name='engine_size',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='engine_type',
            field=models.CharField(choices=[('e', 'Electric'), ('v6', 'V6'), ('i4', 'Inline 4'), ('h', 'Hybrid'), ('v8', 'V8'), ('w8', 'W8'), ('v4', 'V4'), ('i6', 'Inline 6'), ('vr6', 'VR6')], default='i4', max_length=3),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='gas_milage',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='horsepower',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='storage_space',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
