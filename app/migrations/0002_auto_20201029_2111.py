# Generated by Django 2.0.6 on 2020-10-29 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='id_delete',
            new_name='is_delete',
        ),
        migrations.RenameField(
            model_name='authordetail',
            old_name='id_delete',
            new_name='is_delete',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='id_delete',
            new_name='is_delete',
        ),
        migrations.RenameField(
            model_name='press',
            old_name='id_delete',
            new_name='is_delete',
        ),
    ]
