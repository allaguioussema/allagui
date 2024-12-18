from django.contrib import admin

# Register your models here.

from .models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'emotion', 'year', 'rating')
    list_filter = ('emotion', 'year')
    search_fields = ('title', 'description')
    ordering = ('emotion', 'title')