from django.db import models

# Create your models here.

class Movie(models.Model):
    EMOTION_CHOICES = [
        ('disgust', 'Disgust'),
        ('fear', 'Fear'),
        ('happiness', 'Happiness'),
        ('sadness', 'Sadness'),
        ('anger', 'Anger'),
        ('neutral', 'Neutral'),
        ('surprise', 'Surprise')
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    year = models.IntegerField(default=2023)
    emotion = models.CharField(max_length=20, choices=EMOTION_CHOICES, default='neutral')
    image_url = models.URLField(max_length=500, default='https://via.placeholder.com/300x450')
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=7.0)

    def __str__(self):
        return f"{self.title} ({self.emotion})"

    class Meta:
        ordering = ['emotion', 'title']