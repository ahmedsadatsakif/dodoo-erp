# Generated by Django 4.1.2 on 2022-10-25 20:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='for_doctor',
            new_name='of_doctor',
        ),
        migrations.RenameField(
            model_name='workday',
            old_name='for_schedule',
            new_name='of_schedule',
        ),
    ]
