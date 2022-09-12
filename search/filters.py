import django_filters
from django.forms.widgets import TextInput
from django_filters import CharFilter

from .models import *

class OrderFilter(django_filters.FilterSet):
    song = CharFilter(
        widget=TextInput(attrs={'placeholder': 'song', 'class': 'filter-song'}),
        label='',
        lookup_expr='icontains',
        )
    artist = CharFilter(
        widget=TextInput(attrs={'placeholder': 'artist', 'class': 'filter-artist'}),
        label='',
        lookup_expr='icontains',
        )
    annid = CharFilter(
        widget=TextInput(attrs={'placeholder': 'annid', 'class': 'filter-annid'}),
        label='',
        lookup_expr='icontains',
        )
    show = CharFilter(
        widget=TextInput(attrs={'placeholder': 'show', 'class': 'filter-show'}),
        label='',
        lookup_expr='icontains',
        )
    opedin = CharFilter(
        widget=TextInput(attrs={'placeholder': 'opedin', 'class': 'filter-opedin'}),
        label='',
        lookup_expr='icontains',
        )

    class Meta:
        model = AotData
        fields = '__all__'
        exclude = ['mp3', 'h720', 'h480']
