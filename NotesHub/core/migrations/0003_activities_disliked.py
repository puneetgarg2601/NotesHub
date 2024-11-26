# Generated by Django 5.1.3 on 2024-11-26 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_activities'),
    ]

    operations = [
        migrations.AddField(
            model_name='activities',
            name='disliked',
            field=models.IntegerField(choices=[(0, 'Not Disliked'), (1, 'Disliked')], default=0),
        ),
    ]