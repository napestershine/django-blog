# Generated by Django 3.2 on 2021-05-05 18:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20210503_2130'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-published_on']},
        ),
        migrations.AddField(
            model_name='post',
            name='published_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
