# Generated by Django 5.1 on 2024-09-27 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0010_alter_heromodel_hero_class_alter_heromodel_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heromodel',
            name='hero_class',
            field=models.CharField(max_length=20, verbose_name='Class'),
        ),
        migrations.AlterField(
            model_name='heromodel',
            name='nickname',
            field=models.CharField(max_length=20, verbose_name='Name'),
        ),
    ]
