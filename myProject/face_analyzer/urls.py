from django.urls import path
from . import views

urlpatterns = [
    # Web routes
    path('', views.index, name='index'),
    path('analyze/', views.analyze_face, name='analyze_face'),
]
