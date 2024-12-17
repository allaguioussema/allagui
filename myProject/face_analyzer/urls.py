from django.urls import path
from . import views

app_name = 'face_analyzer'

urlpatterns = [
    # Web routes
    path('', views.home, name='home'),  # Home page as default
    path('analyzer/', views.index, name='index'),  # Face analyzer page
    path('analyze/', views.analyze_face, name='analyze_face'),
]
