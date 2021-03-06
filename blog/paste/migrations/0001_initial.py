# Generated by Django 2.2.17 on 2020-11-19 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paste',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15, verbose_name='用户')),
                ('message', models.TextField(verbose_name='信息')),
                ('is_audit', models.BooleanField(default=True, verbose_name='审核')),
                ('publish_time', models.DateTimeField(auto_now_add=True, verbose_name='提交时间')),
            ],
            options={
                'verbose_name': '文本展示',
                'verbose_name_plural': '文本展示',
                'ordering': ['-publish_time'],
            },
        ),
    ]
