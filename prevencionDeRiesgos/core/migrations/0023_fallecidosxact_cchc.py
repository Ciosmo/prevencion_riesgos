# Generated by Django 4.2.6 on 2023-12-11 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_alter_region_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='fallecidosxact',
            name='cchc',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
