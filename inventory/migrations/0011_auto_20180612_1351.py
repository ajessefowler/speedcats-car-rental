# Generated by Django 2.0.6 on 2018-06-12 17:51

from django.db import migrations


class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        ('inventory', '0010_auto_20180611_1840'),
    ]

    operations = [
        migrations.RenameField(
            model_name='store',
            old_name='storeID',
            new_name='ID',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='storeID',
            new_name='store',
        ),
    ]