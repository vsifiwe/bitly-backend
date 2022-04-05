# Generated by Django 4.0.3 on 2022-04-05 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='url',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_url', models.CharField(max_length=100)),
                ('long_url', models.CharField(max_length=200)),
                ('impressions', models.IntegerField()),
            ],
        ),
    ]
