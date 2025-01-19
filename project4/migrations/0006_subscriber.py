# Generated by Django 4.2.17 on 2025-01-19 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project4', '0005_alter_comment_options_alter_post_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('subscribed_on', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['-subscribed_on'],
            },
        ),
    ]
