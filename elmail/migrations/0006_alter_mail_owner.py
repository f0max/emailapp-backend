# Generated by Django 4.1.7 on 2023-05-23 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_smtpuser_name_alter_smtpuser_surname'),
        ('elmail', '0005_mail_owner_alter_mail_body_alter_mail_recipient_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='owner',
            field=models.ForeignKey(db_column='owner_id', on_delete=django.db.models.deletion.DO_NOTHING, to='user.smtpuser'),
        ),
    ]
