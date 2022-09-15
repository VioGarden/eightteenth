from django.http import HttpResponse
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
    """base page of all songs"""
    start_time_filter = time.time() # timing function
    p = Paginator(AotData.objects.all(), 15) # paginates data
    page = request.GET.get('page')
    aot_page = p.get_page(page)
    if request.method == 'POST': # POST request when user adds song to list
        if 'song_primary_key' in request.POST:
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
            return HttpResponse('ajax has broken')
            # render(
            #     request, 'search/song_list.html', {
            #     'aot_page': aot_page, # list of songs
            #     'user_song_already_set': user_song_already_set, # pk set of added elements
            #     'total_time': total_time, # total time
            #     }
            # )
        else:
            return HttpResponse('Did not work')
    elif request.user.is_authenticated: # if user is logged in, clicks onto page
        current_user = request.user # current user
        user_song_list = UserList.objects.all() # list of all songs correlated to user
        user_song_already_set = set() # empty set
        for i in range(len(user_song_list)): # looping over all user songs
            # if the pk of the user song matches current user
            if user_song_list[i].ProfileUser.pk == int(current_user.pk): 
                # pk of that song added to set
                user_song_already_set.add(user_song_list[i].ProfileSong.pk)
        total_time = time.time() - start_time_filter # end timer
        total_time = round(total_time, 5)
        return render(request, 'search/song_list.html', {
                'aot_page': aot_page, # list of songs
                'user_song_already_set': user_song_already_set, # set of pk of added songs
                'total_time': total_time, # total time
            })
    else: # if user not authenticated
        total_time = time.time() - start_time_filter # end timer
        total_time = round(total_time, 5)
        return render(request, 'search/song_list.html', {
            'aot_page': aot_page, # list of songs
            'total_time': total_time, # total time
        })

def filter_search(request):
    """filtered search in database"""
    start_time_filter = time.time() # begin timer
    aot_data = AotData.objects.all() # grab every song in database
    aot_length = len(aot_data) # size of database
    # from search/filters.py, search system
    myFilter = OrderFilter(request.GET, queryset=aot_data) 
    aot_data = myFilter.qs # query search
    user_song_list = UserList.objects.all() # list of all songs in userlist
    if request.method == 'POST': # if method is post, add song button clicked
        song_primary = request.POST.get('song_primary_key') # get song pk
        user_primary = request.POST.get('user_primary_key') # get user pk
        aotsnippet = AotData.objects.get(pk=int(song_primary)) # pull song from database
        usersnippet = MySongUser.objects.get(pk=int(user_primary)) # pull user from database
        usersnippet.my_songs.add(aotsnippet) # add to user list database
        user_song_already_set = set() # create empty set
        for i in range(len(user_song_list)):
            # if the pk of the user song matches current user
            if user_song_list[i].ProfileUser.pk == int(user_primary):
                # pk of that song added to set
                user_song_already_set.add(user_song_list[i].ProfileSong.pk)
        return render(request, 'search/filter_search.html', {
            'myFilter': myFilter, # filter form
            'user_song_already_set': user_song_already_set, # set of user list song pk
        })
    if len(aot_data) == aot_length: #so nothing shows up when nothing is searched
        return render(request, 'search/filter_search.html', {
            'myFilter': myFilter, # filter form
        })
    count = len(aot_data) # number of songs returned, used for search info
    if request.user.is_authenticated: # logged in page reload
        user_song_already_set = set() # create empty set
        for i in range(len(user_song_list)):
            # if the pk of the user song matches current user
            if user_song_list[i].ProfileUser.pk == int(request.user.pk):
                    # pk of that song added to set
                    user_song_already_set.add(user_song_list[i].ProfileSong.pk)
        total_time = time.time() - start_time_filter # timer
        total_time = round(total_time, 5)
        return render(request, 'search/filter_search.html', {
            'myFilter': myFilter, # filter search bar
            'aot_data': aot_data, # list of songs
            'total_time': total_time, # time taken
            'count': count, # number of songs returned
            'user_song_already_set': user_song_already_set, # set of user list pk
        })
    else:
        total_time = time.time() - start_time_filter # end timer
        total_time = round(total_time, 5)
        return render(request, 'search/filter_search.html', {
            'myFilter': myFilter, # filter search bar
            'aot_data': aot_data, # list of songs
            'total_time': total_time, # time taken
            'count': count, # number of songs returns
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
        if 'song_score' in request.POST:
            user_pk = request.user.pk
            song_pk_score = request.POST.get('song_primary_key_score')
            song_score = request.POST.get('song_score')
            for i in range(len(profile_songs)):
                if (profile_songs[i].ProfileUser.pk == int(user_pk) 
                and profile_songs[i].ProfileSong.pk == int(song_pk_score)):
                    score_change_song = profile_songs[i]
                    score_change_song.ProfileScore = int(song_score)
                    score_change_song.save(update_fields=['ProfileScore'])
                    return render(request, 'search/profile.html', {
                        'profile_songs': profile_songs,
                    })
            return render(request, 'search/profile.html', {
                'profile_songs': profile_songs,
            })
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