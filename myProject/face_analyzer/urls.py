from django.urls import path
from . import views
from . import views_auth

app_name = 'face_analyzer'

urlpatterns = [
    # Auth routes
    path('auth/', views_auth.auth_view, name='auth'),
    path('logout/', views_auth.logout_view, name='logout'),
    
    # Web routes
    path('', views.home, name='home'),  # Home page as default
    path('analyzer/', views.index, name='index'),  # Face analyzer page
    path('analyze/', views.analyze_face, name='analyze_face'),
]
