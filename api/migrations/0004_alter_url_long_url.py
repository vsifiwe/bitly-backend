# Generated by Django 4.0.3 on 2022-04-13 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_device'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='long_url',
            field=models.TextField(),
        ),
    ]
