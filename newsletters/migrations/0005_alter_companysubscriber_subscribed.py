# Generated by Django 4.0.8 on 2022-10-31 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletters', '0004_companysubscriber_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companysubscriber',
            name='subscribed',
            field=models.BooleanField(default=True),
        ),
    ]