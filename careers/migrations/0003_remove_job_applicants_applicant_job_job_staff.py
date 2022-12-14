# Generated by Django 4.0.8 on 2023-01-05 09:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('careers', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='applicants',
        ),
        migrations.AddField(
            model_name='applicant',
            name='job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='careers.job'),
        ),
        migrations.AddField(
            model_name='job',
            name='staff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
