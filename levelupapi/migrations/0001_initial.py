# Generated by Django 4.1.6 on 2023-02-02 19:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='GameType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Gamer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('num_players', models.IntegerField()),
                ('maker', models.CharField(max_length=50)),
                ('skill_level', models.IntegerField()),
                ('gamer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='games_created', to='levelupapi.gamer')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', to='levelupapi.gametype')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('datetime', models.DateTimeField()),
                ('address', models.CharField(max_length=155)),
                ('attendees', models.ManyToManyField(through='levelupapi.Attendee', to='levelupapi.gamer')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_events', to='levelupapi.game')),
                ('gamer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organizer_event', to='levelupapi.gamer')),
            ],
        ),
        migrations.AddField(
            model_name='attendee',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registered_gamers', to='levelupapi.event'),
        ),
        migrations.AddField(
            model_name='attendee',
            name='gamer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_registrations', to='levelupapi.gamer'),
        ),
    ]
