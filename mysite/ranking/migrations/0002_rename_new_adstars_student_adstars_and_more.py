# Generated by Django 4.2.7 on 2023-11-12 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranking', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='new_adstars',
            new_name='adstars',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='new_adcoins',
            new_name='current_adcoins',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='new_name',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='student',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
