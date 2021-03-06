# Generated by Django 4.0.4 on 2022-05-27 22:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('borrar_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='dob',
            new_name='date_of_birth',
        ),
        migrations.AlterField(
            model_name='job',
            name='description',
            field=models.TextField(default='', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='job',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to=settings.AUTH_USER_MODEL),
        ),
    ]
