# Generated by Django 4.1.6 on 2023-02-07 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levelupapi', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='num_players',
            new_name='maximum_players',
        ),
        migrations.AddField(
            model_name='game',
            name='minimum_players',
            field=models.IntegerField(default=2),
        ),
    ]
