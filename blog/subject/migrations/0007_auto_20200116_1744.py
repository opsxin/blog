# Generated by Django 2.2.9 on 2020-01-16 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0006_auto_20200116_1736'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='subject',
        ),
        migrations.AddField(
            model_name='contact',
            name='message',
            field=models.TextField(default='', verbose_name='信息'),
            preserve_default=False,
        ),
    ]
