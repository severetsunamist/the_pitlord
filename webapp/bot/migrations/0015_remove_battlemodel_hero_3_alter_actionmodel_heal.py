# Generated by Django 5.1 on 2024-09-30 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0014_alter_heromodel_hero_stage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='battlemodel',
            name='hero_3',
        ),
        migrations.AlterField(
            model_name='actionmodel',
            name='heal',
            field=models.SmallIntegerField(default=0, verbose_name='Heal'),
        ),
    ]
