# Generated by Django 2.0.6 on 2018-06-11 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_auto_20180611_1833'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehicle',
            old_name='store',
            new_name='storeID',
        ),
        migrations.AlterField(
            model_name='store',
            name='storeID',
            field=models.IntegerField(default=0, primary_key=True, serialize=False, unique=True),
        ),
    ]
