import django_filters

from .models import *

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = AotData
        fields = {
            'song': ['icontains'], 
            'artist': ['icontains'], 
            'show': ['icontains'],
            'opedin': ['icontains'],
        }