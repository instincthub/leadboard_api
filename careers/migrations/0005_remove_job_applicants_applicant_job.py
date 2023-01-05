# Generated by Django 4.0.8 on 2023-01-05 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('careers', '0004_remove_applicant_job_remove_job_staff_job_applicants'),
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
    ]
