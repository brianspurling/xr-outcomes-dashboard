# Generated by Django 3.0.4 on 2020-03-28 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_auto_20200328_0604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentary',
            name='commentary_text',
            field=models.TextField(max_length=550),
        ),
    ]
