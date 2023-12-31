# Generated by Django 4.2.6 on 2023-12-11 00:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_accidentesxregion_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accidentesxsexo',
            name='year',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.year'),
        ),
        migrations.AlterField(
            model_name='diasxactividad',
            name='year',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.year'),
        ),
        migrations.AlterField(
            model_name='diasxmut',
            name='year',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.year'),
        ),
        migrations.AlterField(
            model_name='fallecidosxact',
            name='year',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.year'),
        ),
        migrations.AlterField(
            model_name='fallecidosxsexo',
            name='year',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.year'),
        ),
        migrations.AlterField(
            model_name='porcentajexact',
            name='year',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.year'),
        ),
        migrations.AlterField(
            model_name='tasaxact',
            name='year',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.year'),
        ),
    ]
