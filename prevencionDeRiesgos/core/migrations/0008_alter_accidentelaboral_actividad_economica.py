# Generated by Django 4.2.6 on 2023-12-10 05:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_accidentesxsexo_name_remove_tasaxact_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accidentelaboral',
            name='actividad_economica',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.economicactivity'),
        ),
    ]