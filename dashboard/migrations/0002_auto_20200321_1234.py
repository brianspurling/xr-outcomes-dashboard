# Generated by Django 3.0.4 on 2020-03-21 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loadhistory',
            old_name='model_name',
            new_name='table_name',
        ),
    ]