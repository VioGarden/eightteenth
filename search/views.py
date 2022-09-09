import time
from django.shortcuts import render, redirect
from .models import AotData, UserList, MySongUser

from django.core.paginator import Paginator

from .filters import OrderFilter


def song_list(request):
    aot_list = AotData.objects.all()
    p = Paginator(AotData.objects.all(), 15)
    page = request.GET.get('page')
    aot_page = p.get_page(page)
    if request.method == 'POST':
        song_primary = request.POST.get('song_primary_key')
        user_primary = request.POST.get('user_primary_key')
        aotsnippet = AotData.objects.get(pk=int(song_primary))
        usersnippet = MySongUser.objects.get(pk=int(user_primary))
        usersnippet.my_songs.add(aotsnippet)
        user_song_list = UserList.objects.all()
        user_song_pk_set = set()
        for i in range(len(user_song_list)):
            user_song_pk_set.add(user_song_list[i].ProfileSong.pk)
        return render(request, 'search/song_list.html', {
            'song_primary': song_primary,
            'user_primary': user_primary,
            'aot_list': aot_list,
            'aot_page': aot_page,
            'user_song_pk_set': user_song_pk_set,
        })
    else:
        user_song_list = UserList.objects.all()
        user_song_pk_set = set()
        for i in range(len(user_song_list)):
            user_song_pk_set.add(user_song_list[i].ProfileSong.pk)
        return render(request, 'search/song_list.html', {
                'aot_list': aot_list,
                'aot_page': aot_page,
                'user_song_pk_set': user_song_pk_set,
            })

def filter_search(request):

    aot_data = AotData.objects.all()
    aot_length = len(aot_data)

    myFilter = OrderFilter(request.GET, queryset=aot_data)

    aot_data = myFilter.qs
    if len(aot_data) == aot_length: #so nothing shows up when nothing is searched
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
    
def home(request):
    name = "violet"
    return render(request, 'search/home.html', {
        'name': name
    })
    
def profile(request):
    profile_songs = UserList.objects.all()
    if request.method == 'POST':
        song_primary_remove = request.POST.get('song_primary_key_remove')
        user_primary_remove = request.POST.get('user_primary_key_remove')
        aotsnippet_remove = AotData.objects.get(pk=int(song_primary_remove))
        usersnippet_remove = MySongUser.objects.get(pk=int(user_primary_remove))
        usersnippet_remove.my_songs.remove(aotsnippet_remove)
        return render(request, 'search/profile.html', {
            'profile_songs': profile_songs,
            'song_primary_remove': song_primary_remove,
            'user_primary_remove': user_primary_remove,
        })
    else:
        return render(request, 'search/profile.html', {
            'profile_songs': profile_songs,
        })

def quick_search(request):
    start_time = time.time()
    if request.method == 'POST':
        user_song_list = UserList.objects.all()
        user_song_pk_set = set()
        for i in range(len(user_song_list)):
            user_song_pk_set.add(user_song_list[i].ProfileSong.pk)
        if 'searched' in request.POST:
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
                'data_query': data_query,
                'search_type': search_type,
                'count': count,
                'total_time': total_time,
                'user_song_pk_set': user_song_pk_set,
            })
        else: 
            song_primary = request.POST.get('song_primary_key')
            user_primary = request.POST.get('user_primary_key')
            aotsnippet = AotData.objects.get(pk=int(song_primary))
            usersnippet = MySongUser.objects.get(pk=int(user_primary))
            usersnippet.my_songs.add(aotsnippet)
            return render(request, 'search/quick_search.html', {
                'song_primary': song_primary,
                'user_primary': user_primary,
                'user_song_pk_set': user_song_pk_set,
            })
    else:
        return render(request, 'search/quick_search.html', {
        })