import time
from django.shortcuts import render, redirect
from .models import AotData, MySongUser

from django.core.paginator import Paginator

from .filters import OrderFilter


def song_list(request):
    aot_list = AotData.objects.all()
    p = Paginator(AotData.objects.all(), 15)
    page = request.GET.get('page')
    aot_page = p.get_page(page)

    return render(request, 'search/song_list.html', {
        'aot_list': aot_list,
        'aot_page': aot_page,
    })

def filter_search(request):

    aot_data = AotData.objects.all()
    aot_length = len(aot_data)

    myFilter = OrderFilter(request.GET, queryset=aot_data)

    aot_data = myFilter.qs
    if len(aot_data) == aot_length:
        return render(request, 'search/filter_search.html', {
            'myFilter': myFilter,
        })

    # p = Paginator(aot_data, 10)
    # page = request.GET.get('page')
    # aot_page = p.get_page(page)

    return render(request, 'search/filter_search.html', {
        'myFilter': myFilter,
        'aot_data': aot_data,
        # 'aot_page': aot_page,
    })
    

def quick_search(request):
    start_time = time.time()
    if request.method == 'POST':
        search_type = request.POST['search-type']
        searched = request.POST['searched']
        if len(searched) == 0:
            return render(request, 'search/quick_search.html', {})
        if search_type == "song":
            data_query = AotData.objects.filter(song__contains=searched)
        elif search_type == "artist":
            data_query = AotData.objects.filter(artist__contains=searched)
        else:
            data_query = AotData.objects.filter(show__contains=searched)
        count = len(data_query)
        total_time = time.time() - start_time
        total_time = round(total_time, 5)
        return render(request, 'search/quick_search.html', {
            'searched': searched,
            'data': data_query,
            'search_type': search_type,
            'count': count,
            'total_time': total_time,
        })
    else:
        return render(request, 'search/quick_search.html', {
        })

def home(request):
    name = "violet"
    return render(request, 'search/home.html', {
        'name': name
    })

def profile(request):
    profile_songs = MySongUser.objects.all()
    return render(request, 'search/profile.html', {
        'profile_songs': profile_songs
    })

def add_song(request):
    pass