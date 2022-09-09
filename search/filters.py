import django_filters
from django.forms.widgets import TextInput
from django_filters import CharFilter

from .models import *

class OrderFilter(django_filters.FilterSet):
    song = CharFilter(
        widget=TextInput(attrs={'placeholder': 'song'}),
        label='',
        lookup_expr='icontains',
        )
    artist = CharFilter(
        widget=TextInput(attrs={'placeholder': 'artist'}),
        label='',
        lookup_expr='icontains',
        )
    annid = CharFilter(
        widget=TextInput(attrs={'placeholder': 'annid'}),
        label='',
        lookup_expr='icontains',
        )
    show = CharFilter(
        widget=TextInput(attrs={'placeholder': 'show'}),
        label='',
        lookup_expr='icontains',
        )
    opedin = CharFilter(
        widget=TextInput(attrs={'placeholder': 'opedin'}),
        label='',
        lookup_expr='icontains',
        )

    class Meta:
        model = AotData
        fields = '__all__'
        exclude = ['mp3', 'h720', 'h480']
