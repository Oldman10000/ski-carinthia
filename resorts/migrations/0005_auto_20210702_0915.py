# Generated by Django 3.2.4 on 2021-07-02 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resorts', '0004_alter_resort_image_credit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resort',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='resort',
            name='street_address2',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
