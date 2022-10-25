# Generated by Django 4.1.2 on 2022-10-22 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_id', models.CharField(max_length=127, unique=True)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
    ]