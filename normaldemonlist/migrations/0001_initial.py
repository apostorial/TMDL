# Generated by Django 4.2.4 on 2023-12-27 00:24

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NormalLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('levelid', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('publisher', models.CharField(max_length=255)),
                ('ranking', models.PositiveIntegerField(default=0)),
                ('difficulty', models.CharField(choices=[('Hard Demon', 'Hard Demon'), ('Insane Demon', 'Insane Demon'), ('Extreme Demon', 'Extreme Demon')], max_length=255)),
                ('duration', models.CharField(choices=[('Tiny', 'Tiny'), ('Short', 'Short'), ('Medium', 'Medium'), ('Long', 'Long'), ('XL', 'XL')], max_length=255)),
                ('youtube_link', models.URLField(blank=True)),
                ('youtube_thumbnail', models.URLField(blank=True)),
                ('points', models.FloatField(default=0)),
                ('min_points', models.FloatField(default=0)),
                ('min_completion', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)])),
            ],
        ),
        migrations.CreateModel(
            name='NormalRegion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('points', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='NormalPlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('points', models.FloatField(default=0)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='normaldemonlist.normalregion')),
            ],
        ),
        migrations.CreateModel(
            name='NormalListChange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('change_type', models.CharField(choices=[('Place', 'Place'), ('Raise', 'Raise'), ('Lower', 'Lower'), ('Swap', 'Swap'), ('Remove', 'Remove'), ('List requirement', 'List requirement')], default=None, max_length=255)),
                ('placement', models.PositiveIntegerField(default=0)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('effect', models.CharField(blank=True, max_length=255)),
                ('custom_levelname', models.CharField(blank=True, max_length=100, null=True)),
                ('custom_swapwith', models.CharField(blank=True, max_length=100, null=True)),
                ('custom_abovelevelname', models.CharField(blank=True, max_length=100, null=True)),
                ('custom_belowlevelname', models.CharField(blank=True, max_length=100, null=True)),
                ('above_level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='above_level', to='normaldemonlist.normallevel')),
                ('below_level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='below_level', to='normaldemonlist.normallevel')),
                ('level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='normaldemonlist.normallevel')),
                ('swap_with', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='swap_with', to='normaldemonlist.normallevel')),
            ],
        ),
        migrations.AddField(
            model_name='normallevel',
            name='first_victor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='normaldemonlist.normalplayer'),
        ),
        migrations.CreateModel(
            name='NormalLevelRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_percentage', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)])),
                ('record_video_link', models.URLField(blank=True)),
                ('level', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='normaldemonlist.normallevel')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='normaldemonlist.normalplayer')),
            ],
            options={
                'unique_together': {('level', 'player')},
            },
        ),
    ]
