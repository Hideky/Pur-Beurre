# Generated by Django 2.0.2 on 2018-05-12 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='api_token',
            field=models.CharField(max_length=20, null=True),
        ),
    ]