# Generated by Django 5.1.4 on 2024-12-18 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movie',
            options={'ordering': ['emotion', 'title']},
        ),
        migrations.RemoveField(
            model_name='movie',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='image',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='release_date',
        ),
        migrations.AddField(
            model_name='movie',
            name='emotion',
            field=models.CharField(choices=[('disgust', 'Disgust'), ('fear', 'Fear'), ('happiness', 'Happiness'), ('sadness', 'Sadness'), ('anger', 'Anger'), ('neutral', 'Neutral')], default='neutral', max_length=20),
        ),
        migrations.AddField(
            model_name='movie',
            name='image_url',
            field=models.URLField(default='https://via.placeholder.com/300x450', max_length=500),
        ),
        migrations.AddField(
            model_name='movie',
            name='year',
            field=models.IntegerField(default=2023),
        ),
        migrations.AlterField(
            model_name='movie',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=7.0, max_digits=3),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
