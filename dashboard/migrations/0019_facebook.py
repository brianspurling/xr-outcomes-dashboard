# Generated by Django 3.0.4 on 2020-07-24 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0018_auto_20200619_0420'),
    ]

    operations = [
        migrations.CreateModel(
            name='Facebook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('follows_cum', models.IntegerField(blank=True, null=True)),
                ('likes', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
