# Generated by Django 4.2.17 on 2025-01-04 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project4', '0002_post_excerpt'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
