# Generated by Django 4.1.5 on 2023-01-04 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tree_menu', '0004_menu_display_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='url',
            field=models.CharField(max_length=200, verbose_name='URL'),
        ),
    ]
