# Generated by Django 4.1.7 on 2023-05-23 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_smtpuser_name_alter_smtpuser_surname'),
        ('elmail', '0004_alter_mail_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail',
            name='owner',
            field=models.ForeignKey(db_column='login', default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='user.smtpuser'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mail',
            name='body',
            field=models.CharField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='mail',
            name='recipient',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='mail',
            name='sender',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='mail',
            name='subject',
            field=models.CharField(max_length=500),
        ),
    ]
