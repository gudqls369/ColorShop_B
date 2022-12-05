# Generated by Django 4.1.3 on 2022-12-01 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="likes",
        ),
        migrations.AddField(
            model_name="post",
            name="likes",
            field=models.PositiveSmallIntegerField(default=0, verbose_name="Like"),
        ),
    ]
