# Generated by Django 4.1.7 on 2023-05-22 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elmail', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail',
            name='status',
            field=models.CharField(default='sent', max_length=30),
        ),
    ]