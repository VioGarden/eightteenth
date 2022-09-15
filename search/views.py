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
    p = Paginator(AotData.objects.all(), 15) # paginates data, # per page
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
            total_time = round(total_time, 5) # round timer to 5 decimal places
            return HttpResponse('ajax has broken') # this now uses ajax
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
        total_time = round(total_time, 5) # round timer to 5 decimal places
        return render(request, 'search/song_list.html', {
                'aot_page': aot_page, # list of songs
                'user_song_already_set': user_song_already_set, # set of pk of added songs
                'total_time': total_time, # total time
            })
    else: # if user not authenticated
        total_time = time.time() - start_time_filter # end timer
        total_time = round(total_time, 5) # round timer to 5 decimal places
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
        total_time = round(total_time, 5) # round timer to 5 decimal places
        return render(request, 'search/filter_search.html', {
            'myFilter': myFilter, # filter search bar
            'aot_data': aot_data, # list of songs
            'total_time': total_time, # time taken
            'count': count, # number of songs returned
            'user_song_already_set': user_song_already_set, # set of user list pk
        })
    else:
        total_time = time.time() - start_time_filter # end timer
        total_time = round(total_time, 5) # round timer to 5 decimal places
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
    """Profile Page"""
    profile_songs = UserList.objects.all() # grabs every user list project
    if request.method == 'POST':  # post request profile.html
        if 'song_score' in request.POST: # post request for changing score of user song
            user_pk = request.user.pk # current user primary key
            song_pk_score = request.POST.get('song_primary_key_score') # user pk on song
            song_score = request.POST.get('song_score') # get score of song in user list
            # loops over the list of user songs to find matching song of post method
            for i in range(len(profile_songs)):
                # in user list, if the song pk and user pk match
                # the recieved user pk and song pk  (not the score or score pk)
                if (profile_songs[i].ProfileUser.pk == int(user_pk) 
                and profile_songs[i].ProfileSong.pk == int(song_pk_score)):
                    score_change_song = profile_songs[i] # initialize user list song
                    score_change_song.ProfileScore = int(song_score) # set score to score
                    score_change_song.save(update_fields=['ProfileScore']) # update field
                    return render(request, 'search/profile.html', {
                        # return updated profile songs, will be updated
                        'profile_songs': profile_songs, 
                    })
            return render(request, 'search/profile.html', {
                # if no matches are found for some reason, still returns page
                # profile songs is list of all user list songs
                # html page does the sorting if should be displayed or not
                'profile_songs': profile_songs,
            })
        # below is scenario where user removes song
        song_primary_remove = request.POST.get('song_primary_key_remove') # pk of song
        user_primary_remove = request.POST.get('user_primary_key_remove') # user pk
        # find query of song to remove in the database
        aotsnippet_remove = AotData.objects.get(pk=int(song_primary_remove)) 
        # find query of user of the song to remove from database
        usersnippet_remove = MySongUser.objects.get(pk=int(user_primary_remove))
        # from MySongUser not UserList because of model relationship in models
        # uservar.my_songs.all() is a queryset for every song under that user
        # remove the queryed song from the specified user's list of songs
        usersnippet_remove.my_songs.remove(aotsnippet_remove)
        return render(request, 'search/profile.html', {
            'profile_songs': profile_songs, # return all profile songs
        })
    else:
        # on page load
        return render(request, 'search/profile.html', {
            # return all user songs
            'profile_songs': profile_songs, 
        })

def quick_search(request):
    """one input search method"""
    start_time = time.time() # start timer
    if request.method == 'POST': 
        if 'searched' in request.POST: # scenario if user searches in search bar
             # gets data category (options: song, artist, or show)
            search_type = request.POST['search-type']
            # gets searched query
            searched = request.POST['searched']
            if len(searched) == 0: # if nothing searched, return no matches
                return render(request, 'search/quick_search.html', {})
            if search_type == "song": # where model element name is song
                data_query = AotData.objects.filter(song__contains=searched)
            elif search_type == "artist": # where model element name is artist
                data_query = AotData.objects.filter(artist__contains=searched)
            else: # where model element name is show (no other options are givwn)
                data_query = AotData.objects.filter(show__contains=searched)
            count = len(data_query) # length of the number of matches for a specific query
            if request.user.is_authenticated: # want to send add to list option if authenticated
                user_song_list = UserList.objects.all() # list of all user list objects
                user_primary = request.user.pk # user pk
                user_song_already_set = set() # initialize set
                for i in range(len(user_song_list)): 
                    # if the pk of the user song matches current user
                    if user_song_list[i].ProfileUser.pk == int(user_primary):
                        # pk of that song added to set
                        user_song_already_set.add(user_song_list[i].ProfileSong.pk)
                total_time = time.time() - start_time # end timer
                total_time = round(total_time, 5) # round timer to 5 decimal places
                return render(request, 'search/quick_search.html', {
                    'searched': searched, # what user inputted
                    'data_query': data_query, # list of matching songs
                    'count': count, # how many results returned
                    'total_time': total_time, # how long it took to search
                    'user_song_already_set': user_song_already_set, # set of pk values
                })
            else: # if user is not authenticated
                total_time = time.time() - start_time # end timer
                total_time = round(total_time, 5) # round timer to 5 decimal places
                return render(request, 'search/quick_search.html', {
                    'searched': searched, # what user inputted
                    'data_query': data_query, # return data query of songs
                    'count': count, # return number of songs
                    'total_time': total_time, # return time taken
                })
        else: # scenario for post request where user adds song to their user list
            song_primary = request.POST.get('song_primary_key') # get pk of song
            user_primary = request.POST.get('user_primary_key') # get user pk
            aotsnippet = AotData.objects.get(pk=int(song_primary)) # find matching song query
            usersnippet = MySongUser.objects.get(pk=int(user_primary)) # find correct user
            usersnippet.my_songs.add(aotsnippet) # add song to user's list of songs
            user_song_list = UserList.objects.all() # list of every song by user
            user_song_already_set = set() # initialize set
            for i in range(len(user_song_list)): 
                # if the pk of the user song matches current user
                if user_song_list[i].ProfileUser.pk == int(user_primary):
                    # pk of that song added to set
                    user_song_already_set.add(user_song_list[i].ProfileSong.pk)
            return render(request, 'search/quick_search.html', {
                'song_primary': song_primary,
                'user_primary': user_primary,
                'user_song_already_set': user_song_already_set,
            })
    else:
        return render(request, 'search/quick_search.html', {
        })