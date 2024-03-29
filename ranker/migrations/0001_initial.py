# Generated by Django 3.2.9 on 2021-11-15 04:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('current_rating', models.IntegerField(default=1000)),
                ('artwork', models.CharField(blank=True, max_length=250, null=True)),
                ('star_rating', models.PositiveSmallIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('winner_rating', models.IntegerField()),
                ('loser_rating', models.IntegerField()),
                ('loser', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='matches_lost', to='ranker.album')),
                ('winner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='matches_won', to='ranker.album')),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ranker.artist'),
        ),
    ]
