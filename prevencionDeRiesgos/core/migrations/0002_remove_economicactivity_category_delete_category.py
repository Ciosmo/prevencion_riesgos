# Generated by Django 4.2.6 on 2023-10-29 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='economicactivity',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]