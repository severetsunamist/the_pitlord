# Generated by Django 5.1 on 2024-09-18 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_battlemodel_queue_alter_heromodel_hero_class_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heromodel',
            name='hero_class',
            field=models.CharField(default='Archer', max_length=20, verbose_name='Class'),
        ),
        migrations.AlterField(
            model_name='heromodel',
            name='nickname',
            field=models.CharField(default='Elder Joe', max_length=20, verbose_name='Name'),
        ),
    ]
