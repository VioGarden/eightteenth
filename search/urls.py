from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quick_search/', views.quick_search, name='quick-search'),
    path('song_list/', views.song_list, name='song-list'),
    path('filter_search/', views.filter_search, name='filter-search'),
    path('profile/', views.profile, name='profile'),
]
