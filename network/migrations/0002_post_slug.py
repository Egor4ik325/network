# Generated by Django 3.2.6 on 2021-08-12 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(null=True, unique=True, verbose_name='Post slug from title'),
        ),
    ]