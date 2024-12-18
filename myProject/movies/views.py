from django.shortcuts import render
from .models import Movie
from django.db.models import Q
import json

def index(request):
    # Get all unique emotions for the filter buttons
    emotions = [choice[0] for choice in Movie.EMOTION_CHOICES]
    
    # Get emotion data from query params
    emotion_data = request.GET.get('emotion_data')
    selected_emotion = request.GET.get('emotion')
    
    # Get all movies first
    all_movies = Movie.objects.all()
    print(f"Total movies in database: {all_movies.count()}")
    
    if emotion_data:
        try:
            # Parse emotion data (format: {"happy": 0.6, "neutral": 0.2, "sad": 0.2})
            emotion_scores = json.loads(emotion_data)
            print(f"Received emotion scores: {emotion_scores}")
            
            # Filter emotions with at least 5% representation
            MIN_PERCENTAGE = 0.05
            filtered_emotions = {
                emotion: score 
                for emotion, score in emotion_scores.items() 
                if score >= MIN_PERCENTAGE
            }
            
            if not filtered_emotions:
                # If no emotion has >= 5%, take the highest one
                max_emotion = max(emotion_scores.items(), key=lambda x: x[1])
                filtered_emotions = {max_emotion[0]: max_emotion[1]}
            
            # Normalize scores to sum to 1
            total_score = sum(filtered_emotions.values())
            normalized_emotions = {
                emotion: score/total_score 
                for emotion, score in filtered_emotions.items()
            }
            
            print(f"Filtered emotions (>=5%): {filtered_emotions}")
            print(f"Normalized emotions: {normalized_emotions}")
            
            # Sort emotions by score in descending order
            sorted_emotions = sorted(normalized_emotions.items(), key=lambda x: x[1], reverse=True)
            print(f"Sorted emotions: {sorted_emotions}")
            
            # Calculate number of movies to fetch for each emotion
            total_movies = 10
            recommended_movies = []
            
            for emotion, score in sorted_emotions:
                # Calculate number of movies for this emotion
                num_movies = max(1, int(round(score * total_movies)))
                # Get random movies for this emotion
                emotion_movies = list(Movie.objects.filter(emotion__iexact=emotion.lower()).order_by('?')[:num_movies])
                print(f"Found {len(emotion_movies)} movies for emotion {emotion} (score: {score:.1%})")
                recommended_movies.extend(emotion_movies)
            
            # If we have less than 10 movies, add more from top emotion
            if len(recommended_movies) < total_movies and sorted_emotions:
                top_emotion = sorted_emotions[0][0]
                additional_movies = list(Movie.objects.filter(emotion__iexact=top_emotion.lower())
                                      .exclude(id__in=[m.id for m in recommended_movies])
                                      .order_by('?')[:total_movies - len(recommended_movies)])
                recommended_movies.extend(additional_movies)
            
            movies = recommended_movies
            print(f"Total recommended movies: {len(movies)}")
            
        except json.JSONDecodeError as e:
            print(f"Error decoding emotion data: {e}")
            movies = all_movies
    elif selected_emotion:
        # If only single emotion is selected
        movies = Movie.objects.filter(emotion__iexact=selected_emotion.lower())
        print(f"Found {movies.count()} movies for emotion {selected_emotion}")
    else:
        # Show all movies if no emotion is selected
        movies = all_movies
        print(f"Showing all {movies.count()} movies")
    
    context = {
        'movies': movies,
        'emotions': emotions,
        'selected_emotion': selected_emotion,
        'emotion_data': emotion_data  # Pass the original emotion data for display
    }
    
    return render(request, 'movies/index.html', context)