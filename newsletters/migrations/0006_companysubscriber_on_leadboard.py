# Generated by Django 4.0.8 on 2022-10-31 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletters', '0005_alter_companysubscriber_subscribed'),
    ]

    operations = [
        migrations.AddField(
            model_name='companysubscriber',
            name='on_leadboard',
            field=models.BooleanField(default=False),
        ),
    ]
