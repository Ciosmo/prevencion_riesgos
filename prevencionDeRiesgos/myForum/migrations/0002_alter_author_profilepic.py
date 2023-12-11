# Generated by Django 4.2.7 on 2023-12-11 16:13

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('myForum', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='profilePic',
            field=django_resized.forms.ResizedImageField(crop=None, default=None, force_format=None, keep_meta=True, null=True, quality=100, scale=None, size=[50, 80], upload_to='myForum/media/authors/'),
        ),
    ]
