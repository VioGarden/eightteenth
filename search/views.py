import time
from django.shortcuts import render
from .models import AotData, UserList, MySongUser
from django.core.paginator import Paginator
from .filters import OrderFilter

"""
Models-
AotData : Database of every song
MySongUser : Database of every user
UserList : Database of added songs (list of user-song matches)
"""

def song_list(request):
    start_time_filter = time.time() # timing function
    aot_list = AotData.objects.all() # every song grabbed
    p = Paginator(AotData.objects.all(), 15) # paginates data
    page = request.GET.get('page')
    aot_page = p.get_page(page)
    if request.method == 'POST': # POST request when user adds song to list
        song_primary = request.POST.get('song_primary_key') # get song pk
        user_primary = request.POST.get('user_primary_key') # get user pk
        aotsnippet = AotData.objects.get(pk=int(song_primary)) # get added song from database
        usersnippet = MySongUser.objects.get(pk=int(user_primary)) # get user from database
        usersnippet.my_songs.add(aotsnippet) # add song to user database
        user_song_list = UserList.objects.all() # get all user songs
        # create a set
        user_song_already_set = set()
        # foor loop iterates over every user song and if the user pk matches the
        # current users pk, the pk of the song is added to a set.
        # set is needed so that users cannot re-add song to their list
        for i in range(len(user_song_list)): # loops over every user song 
            # if the pk of the user song matches current user
            if user_song_list[i].ProfileUser.pk == int(user_primary): 
                # pk of that song added to set
                user_song_already_set.add(user_song_list[i].ProfileSong.pk)
        total_time = time.time() - start_time_filter # end timer
        total_time = round(total_time, 5)
        return render(request, 'search/song_list.html', {
            'aot_page': aot_page,
            'user_song_already_set': user_song_already_set,
            'total_time': total_time,
        })
    elif request.user.is_authenticated:
        #get primary key on window load
        current_user = request.user
        user_song_list = UserList.objects.all()
        user_song_already_set = set()
        #for loop below increases time by 10x
        for i in range(len(user_song_list)):
            if user_song_list[i].ProfileUser.pk == int(current_user.pk):
                user_song_already_set.add(user_song_list[i].ProfileSong.pk)
        total_time = time.time() - start_time_filter
        total_time = round(total_time, 5)
        return render(request, 'search/song_list.html', {
                'aot_list': aot_list,
                'aot_page': aot_page,
                'user_song_already_set': user_song_already_set,
                'total_time': total_time,
            })
    else:
        total_time = time.time() - start_time_filter
        total_time = round(total_time, 5)
        return render(request, 'search/song_list.html', {
            'aot_page': aot_page,
            'total_time': total_time,
        })

def filter_search(request):
    start_time_filter = time.time()
    aot_data = AotData.objects.all()
    aot_length = len(aot_data)

    myFilter = OrderFilter(request.GET, queryset=aot_data)

    aot_data = myFilter.qs

    user_song_list = UserList.objects.all()
    user_song_pk_set = set()
    for i in range(len(user_song_list)):
        user_song_pk_set.add(user_song_list[i].ProfileSong.pk)
    
    if request.method == 'POST':
        song_primary = request.POST.get('song_primary_key')
        user_primary = request.POST.get('user_primary_key')
        aotsnippet = AotData.objects.get(pk=int(song_primary))
        usersnippet = MySongUser.objects.get(pk=int(user_primary))
        usersnippet.my_songs.add(aotsnippet)
        user_song_already_set = set()
        #for loop below increases time by 10x
        for i in range(len(user_song_list)):
            if user_song_list[i].ProfileUser.pk == int(user_primary):
                user_song_already_set.add(user_song_list[i].ProfileSong.pk)
        return render(request, 'search/filter_search.html', {
            'myFilter': myFilter,
            'song_primary': song_primary,
            'user_primary': user_primary,
            'user_song_already_set': user_song_already_set,
        })

    if len(aot_data) == aot_length: #so nothing shows up when nothing is searched
        return render(request, 'search/filter_search.html', {
            'myFilter': myFilter,
        })

    # p = Paginator(aot_data, 10)
    # page = request.GET.get('page')
    # aot_page = p.get_page(page)
    total_time = time.time() - start_time_filter
    total_time = round(total_time, 5)
    count = len(aot_data)
    if request.user.is_authenticated:
        #count = one/1 scenario
        user_song_already_set = set()
        #for loop below increases time by 10x
        for i in range(len(user_song_list)):
            if user_song_list[i].ProfileUser.pk == int(request.user.pk):
                    user_song_already_set.add(user_song_list[i].ProfileSong.pk)
        return render(request, 'search/filter_search.html', {
            'myFilter': myFilter,
            'aot_data': aot_data,
            'total_time': total_time,
            'count': count,
            'user_song_already_set': user_song_already_set,
            # 'aot_page': aot_page,
        })
    else:
        return render(request, 'search/filter_search.html', {
            'myFilter': myFilter,
            'aot_data': aot_data,
            'total_time': total_time,
            'count': count,
        })

    
def home(request):
    name = "violet"
    return render(request, 'search/home.html', {
        'name': name
    })
    
def profile(request):
    #something to search profile songs
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
        if 'searched' in request.POST:
            search_type = request.POST['search-type']
            searched = request.POST['searched']
            user_pk = request.POST.get('quick_search_pk')
            if len(searched) == 0:
                return render(request, 'search/quick_search.html', {})
            if search_type == "song":
                data_query = AotData.objects.filter(song__contains=searched)
            elif search_type == "artist":
                data_query = AotData.objects.filter(artist__contains=searched)
            else:
                data_query = AotData.objects.filter(show__contains=searched)
            count = len(data_query)
            if request.user.is_authenticated:
                user_song_list = UserList.objects.all()
                user_primary = request.user.pk
                user_song_already_set = set()
                #for loop below increases time by 10x
                for i in range(len(user_song_list)):
                    if user_song_list[i].ProfileUser.pk == int(user_primary):
                        user_song_already_set.add(user_song_list[i].ProfileSong.pk)
                total_time = time.time() - start_time
                total_time = round(total_time, 5)
                return render(request, 'search/quick_search.html', {
                    'searched': searched,
                    'data_query': data_query,
                    'search_type': search_type,
                    'count': count,
                    'total_time': total_time,
                    'user_song_already_set': user_song_already_set,
                })
            else:
                total_time = time.time() - start_time
                total_time = round(total_time, 5)
                return render(request, 'search/quick_search.html', {
                    'data_query': data_query,
                    'count': count,
                    'total_time': total_time,
                })
        else: 
            song_primary = request.POST.get('song_primary_key')
            user_primary = request.POST.get('user_primary_key')
            aotsnippet = AotData.objects.get(pk=int(song_primary))
            usersnippet = MySongUser.objects.get(pk=int(user_primary))
            usersnippet.my_songs.add(aotsnippet)
            user_song_list = UserList.objects.all()
            user_song_pk_set = set()
            for i in range(len(user_song_list)):
                # if user_song_list[i].ProfileUser.pk != user_pk:
                user_song_pk_set.add(user_song_list[i].ProfileSong.pk)
            return render(request, 'search/quick_search.html', {
                'song_primary': song_primary,
                'user_primary': user_primary,
                'user_song_pk_set': user_song_pk_set,
            })
    else:
        return render(request, 'search/quick_search.html', {
        })