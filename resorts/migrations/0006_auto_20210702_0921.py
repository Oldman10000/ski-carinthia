# Generated by Django 3.2.4 on 2021-07-02 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resorts', '0005_auto_20210702_0915'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resort',
            old_name='street_address1',
            new_name='street_address_1',
        ),
        migrations.RenameField(
            model_name='resort',
            old_name='street_address2',
            new_name='street_address_2',
        ),
    ]