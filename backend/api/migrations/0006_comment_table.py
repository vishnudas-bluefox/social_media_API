# Generated by Django 4.1.3 on 2022-11-30 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='comment_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.IntegerField(default=0)),
                ('user_id', models.IntegerField(default=0)),
                ('comment', models.CharField(max_length=250)),
            ],
        ),
    ]
