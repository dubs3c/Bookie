# Generated by Django 3.2.16 on 2023-01-10 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0023_auto_20200206_2340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmarks',
            name='image',
            field=models.TextField(blank=True, null=True),
        ),
    ]
