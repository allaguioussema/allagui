from django.shortcuts import render
from .models import Movie

# Create your views here.

def index(request):
    # Get emotion filter from query params
    selected_emotion = request.GET.get('emotion', None)
    
    # Get all unique emotions
    emotions = [choice[0] for choice in Movie.EMOTION_CHOICES]
    
    # Filter movies by emotion if selected
    if selected_emotion:
        movies = Movie.objects.filter(emotion=selected_emotion)
    else:
        movies = Movie.objects.all()
    
    context = {
        'movies': movies,
        'emotions': emotions,
        'selected_emotion': selected_emotion
    }
    
    return render(request, 'movies/index.html', context)