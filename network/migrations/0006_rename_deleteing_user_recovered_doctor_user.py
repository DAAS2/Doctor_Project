# Generated by Django 4.2.7 on 2023-11-07 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_recovered_doctor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recovered_doctor',
            old_name='deleteing_user',
            new_name='user',
        ),
    ]
