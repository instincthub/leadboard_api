# Generated by Django 4.0.8 on 2022-11-02 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0007_leadcontact_want_alter_leadcontact_category_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='leadcontact',
            options={'ordering': ['-timestamp']},
        ),
    ]