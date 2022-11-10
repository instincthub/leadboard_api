# Generated by Django 4.0.8 on 2022-11-08 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('careers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='email',
            field=models.EmailField(default='dev.codertjay@gmail.com', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='applicant',
            name='image',
            field=models.ImageField(default='C:\\', upload_to='applicants'),
            preserve_default=False,
        ),
    ]
