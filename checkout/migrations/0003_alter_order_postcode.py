# Generated by Django 3.2.4 on 2021-07-08 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_auto_20210708_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='postcode',
            field=models.CharField(default='', max_length=20),
        ),
    ]