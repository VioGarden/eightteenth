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
    start_time_filter = time.time() # timing function
    profile_songs = UserList.objects.all() # grabs every user list project
    if request.method == 'POST':  # post request profile.html
        if 'profile-order-type' in request.POST:
            order_method = request.POST['profile-order-type']
            if order_method == 'added-order-old':  #default, Old --> New
                profile_songs = profile_songs.order_by('ProfileSong')
            elif order_method == 'added-order-new':  #flip default, New --> Old
                profile_songs = profile_songs.order_by('-ProfileSong')
            elif order_method == 'song-score-hl': # song score, High --> Low ("None" at bottom)
                profile_songs = profile_songs.order_by('-ProfileScore')
            elif order_method == 'song-score-lh':  #song score, Low --> High ("None" at top)
                profile_songs = profile_songs.order_by('ProfileScore')
            elif order_method == 'song-az': # if song-az
                song_az_set = [] # empty list
                # getting a list of all songs of specific user
                profile_songsaz = UserList.objects.filter(ProfileUser = request.user.pk)
                # loop over user songs
                for i in profile_songsaz:
                    # add song and primary key to set
                    song_az_set.append((i.ProfileSong.song, i.ProfileSong.pk))
                # sorts the set by song, alphabetical ordering
                song_az_set.sort(key=lambda tup: tup[0].lower())
                # profile_songs will be returned
                profile_songs = []
                # looping over alphabetically ordered set
                for j in range(len(song_az_set)):
                    # find the song in all user's songs
                    for k in range(len(profile_songsaz)):
                        # find match by primary key
                        if song_az_set[j][1] == profile_songsaz[k].ProfileSong.pk:
                            # append the query to the profile_songs list
                            profile_songs.append(profile_songsaz[k])
            elif order_method == 'song-za': # opposite alphabetical order
                song_za_set = []
                # getting a list of all songs of specific user
                profile_songsza = UserList.objects.filter(ProfileUser = request.user.pk)
                # loop over user songs
                for i in profile_songsza:
                    # add song and primary key to set
                    song_za_set.append((i.ProfileSong.song, i.ProfileSong.pk))
                # sorts the set by song, anti-alphabetical ordering
                song_za_set.sort(key=lambda tup: tup[0].lower(), reverse=True)
                profile_songs = []
                # looping over anti-alphabetically ordered set
                for j in range(len(song_za_set)):
                    # find the song in all user's songs
                    for k in range(len(profile_songsza)):
                        # find match by primary key
                        if song_za_set[j][1] == profile_songsza[k].ProfileSong.pk:
                            # append the query to the profile_songs list
                            profile_songs.append(profile_songsza[k])
            elif order_method == 'artist-az': # alphabetical order artists
                artist_az_set = []
                # getting a list of all songs of specific user
                profile_artistsaz = UserList.objects.filter(ProfileUser = request.user.pk)
                # loop over user songs
                for i in profile_artistsaz:
                    # add song and primary key to set
                    artist_az_set.append((i.ProfileSong.artist, i.ProfileSong.pk))
                # sorts the set by artists, alphabetical ordering
                artist_az_set.sort(key=lambda tup: tup[0].lower())
                profile_artists = []
                # looping over alphabetically ordered set
                for j in range(len(artist_az_set)):
                    # find the song in all user's songs
                    for k in range(len(profile_artistsaz)):
                        # find match by primary key
                        if artist_az_set[j][1] == profile_artistsaz[k].ProfileSong.pk:
                             # append the query to the profile_artists list
                            profile_artists.append(profile_artistsaz[k])
                # match variable to profile_songs so data can be returned
                profile_songs = profile_artists
            elif order_method == 'artist-za': # anti-alphabetical order artists
                artist_za_set = []
                # getting a list of all songs of specific user
                profile_artistsza = UserList.objects.filter(ProfileUser = request.user.pk)
                # loop over user songs
                for i in profile_artistsza:
                    # add song and primary key to set
                    artist_za_set.append((i.ProfileSong.artist, i.ProfileSong.pk))
                # sorts the set by artists, anti-alphabetical ordering
                artist_za_set.sort(key=lambda tup: tup[0].lower(), reverse=True)
                profile_artists = []
                # looping over anti-alphabetically ordered set
                for j in range(len(artist_za_set)):
                    # find the song in all user's songs
                    for k in range(len(profile_artistsza)):
                         # find match by primary key
                        if artist_za_set[j][1] == profile_artistsza[k].ProfileSong.pk:
                            # append the query to the profile_artists list
                            profile_artists.append(profile_artistsza[k])
                # match variable to profile_songs so data can be returned
                profile_songs = profile_artists
            elif order_method == 'show-az': # alphabetical order shows
                show_az_set = []
                # getting a list of all songs of specific user
                profile_showsaz = UserList.objects.filter(ProfileUser = request.user.pk)
                # loop over user songs
                for i in profile_showsaz:
                    # add song and primary key to set
                    show_az_set.append((i.ProfileSong.show, i.ProfileSong.pk))
                # sorts the set by show, alphabetical ordering
                show_az_set.sort(key=lambda tup: tup[0].lower())
                profile_shows = []
                # looping over alphabetically ordered set
                for j in range(len(show_az_set)):
                    # find the song in all user's songs
                    for k in range(len(profile_showsaz)):
                        # find match by primary key
                        if show_az_set[j][1] == profile_showsaz[k].ProfileSong.pk:
                            # append the query to the profile_shows list
                            profile_shows.append(profile_showsaz[k])
                # match variable to profile_songs so data can be returned
                profile_songs = profile_shows
            elif order_method == 'show-za': # anti-alphabetical order shows
                show_za_set = []
                # getting a list of all songs of specific user
                profile_showsza = UserList.objects.filter(ProfileUser = request.user.pk)
                # loop over user songs
                for i in profile_showsza:
                    # add song and primary key to set
                    show_za_set.append((i.ProfileSong.show, i.ProfileSong.pk))
                # sorts the set by show, anti-alphabetical ordering
                show_za_set.sort(key=lambda tup: tup[0].lower(), reverse=True)
                profile_shows = []
                # looping over anti-alphabetically ordered set
                for j in range(len(show_za_set)):
                    # find the song in all user's songs
                    for k in range(len(profile_showsza)):
                        # find match by primary key
                        if show_za_set[j][1] == profile_showsza[k].ProfileSong.pk:
                            # append the query to the profile_shows list
                            profile_shows.append(profile_showsza[k])
                # match variable to profile_songs so data can be returned
                profile_songs = profile_shows
            total_time = time.time() - start_time_filter # end timer
            total_time = round(total_time, 5) # round timer to 5 decimal places
            return render(request, 'search/profile.html', {
                'profile_songs': profile_songs, # ordered list of profile songs
                'cp1': order_method, # method/type of order
                'total_time': total_time, # time taken to order
            })
        elif 'song_primary_key_remove' in request.POST: # scenerio where user adds to song list
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
            return HttpResponse('Removed song')
        elif 'song_score' in request.POST: # post request for changing score of user song
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
        else:
            return HttpResponse('VioletMiko')
    else:
        # on page load
        # profile_songs = set(profile_songs)
        total_time = time.time() - start_time_filter # end timer
        total_time = round(total_time, 5) # round timer to 5 decimal places
        return render(request, 'search/profile.html', {
            # return all user songs
            'profile_songs': profile_songs, 
            'total_time': total_time,
        })

def quick_search(request):
    """one input search method"""
    start_time = time.time() # start timer
    if request.method == 'POST': 
        if 'song_primary_key' in request.POST: # scenerio where user adds to song list
            song_primary = request.POST.get('song_primary_key') # get song pk
            user_primary = request.POST.get('user_primary_key') # get user pk
            aotsnippet = AotData.objects.get(pk=int(song_primary)) # pull song from database
            usersnippet = MySongUser.objects.get(pk=int(user_primary)) # pull user from database
            usersnippet.my_songs.add(aotsnippet) # add to user list database
            user_song_list = UserList.objects.all() # list of all songs in userlist
            user_song_already_set = set() # create empty set
            for i in range(len(user_song_list)):
                # if the pk of the user song matches current user
                if user_song_list[i].ProfileUser.pk == int(user_primary):
                    # pk of that song added to set
                    user_song_already_set.add(user_song_list[i].ProfileSong.pk)
            return HttpResponse('Added')  # **will use ajax so don't worry for now**
        elif 'searched' in request.POST: # scenario if user searches in search bar
            # gets data category (options: song, artist, or show)
            search_type = request.POST['search-type']
            # gets searched query
            searched = request.POST['searched']
            if len(searched) == 0: # if nothing searched, return no matches
                return render(request, 'search/quick_search.html', {
                    # blank search is a return case
                })
            if search_type == "song": # where model element name is song
                data_query = AotData.objects.filter(song__contains=searched)
            elif search_type == "artist": # where model element name is artist
                data_query = AotData.objects.filter(artist__contains=searched)
            else: # where model element name is show (no other options are givwn)
                data_query = AotData.objects.filter(show__contains=searched)
            count = len(data_query) # length of the number of matches for a specific query
            if request.user.is_authenticated: # want to send add to list option if authenticated
                user_song_list = UserList.objects.all() # list of all songs in userlist
                user_song_already_set = set() # create empty set
                user_primary = request.user.pk
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
            else: # if user is not autheticated, don't need add to song list method
                total_time = time.time() - start_time # end timer
                total_time = round(total_time, 5) # round timer to 5 decimal places
                return render(request, 'search/quick_search.html', {
                    'searched': searched, # what user inputted
                    'data_query': data_query, # return data query of songs
                    'count': count, # return number of songs
                    'total_time': total_time, # return time taken
                })
        else: # scenario for post request where user adds song to their user list
            return HttpResponse('Sorry, Post Request Went Wrong')
    else: # not results returns upon page load
        return render(request, 'search/quick_search.html', {
        })