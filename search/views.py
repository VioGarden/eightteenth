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

def order_profile_songs(query_set, list_title_i):
    """
    this function sorts a query set by looking at a list which has the desired order

    query_set = set of all songs specific to current user in a query set
    list_title_i = the query set sorted as a list with element bieng a tuple of item and index
    """
    # why necessary : have not been able to find an order command for 
    # items that are related to django models by foreign keys, hence manual order is necessary
    profile_songs = []
    # for each item in list
    for j in range(len(list_title_i)):
        # loop over the query set
        for k in range(len(query_set)):
            # if the item in list is found in the query set
            if list_title_i[j][1] == query_set[k].ProfileSong.pk:
                # append that element to a list of queries
                profile_songs.append(query_set[k])
    return profile_songs


def already(usl, up):
    """
    creates a set that of primary keys of songs
    which the user has in their song list

    in html, these songs in the set will not have a "+" option
    because they are already in the user's song list

    usl = usersonglist (list of every song that has been added by all users)
    up = current user's primary key
    """
    already_set = set()
    # iterates over every song that is in usersonglist
    for i in range(len(usl)):
        # if the song's profileuser's primary key matches current user's pk
        if usl[i].ProfileUser.pk == int(up):
            # thta song is added to the set
            already_set.add(usl[i].ProfileSong.pk)
    return already_set

def song_list(request):
    """base page of all songs"""
    start_time_filter = time.time() # timing function
    p = Paginator(AotData.objects.all(), 100) # paginates data, # per page
    page = request.GET.get('page')
    aot_page = p.get_page(page)
    if request.method == 'POST': # POST request when user adds song to list
        if 'song_primary_key' in request.POST:
            return HttpResponse('ajax has broken') # this now uses ajax
        else:
            return HttpResponse('Did not work')
    elif request.user.is_authenticated: # if user is logged in, clicks onto page
        current_user = request.user.pk # current user
        user_song_list = UserList.objects.all() # list of all songs correlated to user
        user_song_already_set = already(user_song_list, current_user) # function already
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
        user_song_already_set = already(user_song_list, user_primary) # function already
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
        current_user = request.user.pk
        user_song_already_set = already(user_song_list, current_user) # function already
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
                # getting a list of all songs of specific user
                profile_songsaz = UserList.objects.filter(ProfileUser = request.user.pk)
                song_az_set = [] # empty list
                # loop over user songs
                for i in profile_songsaz:
                    # add song and primary key to set
                    song_az_set.append((i.ProfileSong.song, i.ProfileSong.pk))
                # sorts the set by song, alphabetical ordering
                song_az_set.sort(key=lambda tup: tup[0].lower())
                # function to make list of displayable songs
                profile_songs = order_profile_songs(profile_songsaz, song_az_set)
            elif order_method == 'song-za': # opposite alphabetical order
                # getting a list of all songs of specific user
                profile_songsza = UserList.objects.filter(ProfileUser = request.user.pk)
                song_za_set = []
                # loop over user songs
                for i in profile_songsza:
                    # add song and primary key to set
                    song_za_set.append((i.ProfileSong.song, i.ProfileSong.pk))
                # sorts the set by song, anti-alphabetical ordering
                song_za_set.sort(key=lambda tup: tup[0].lower(), reverse=True)
                # function to make list of displayable songs
                profile_songs = order_profile_songs(profile_songsza, song_za_set)
            elif order_method == 'artist-az': # alphabetical order artists
                # getting a list of all songs of specific user
                profile_artistsaz = UserList.objects.filter(ProfileUser = request.user.pk)
                artist_az_set = []
                # loop over user songs
                for i in profile_artistsaz:
                    # add song and primary key to set
                    artist_az_set.append((i.ProfileSong.artist, i.ProfileSong.pk))
                # sorts the set by artists, alphabetical ordering
                artist_az_set.sort(key=lambda tup: tup[0].lower())
                # function to make list of displayable songs
                profile_songs = order_profile_songs(profile_artistsaz, artist_az_set)
            elif order_method == 'artist-za': # anti-alphabetical order artists
                # getting a list of all songs of specific user
                artist_za_set = []
                profile_artistsza = UserList.objects.filter(ProfileUser = request.user.pk)
                # loop over user songs
                for i in profile_artistsza:
                    # add song and primary key to set
                    artist_za_set.append((i.ProfileSong.artist, i.ProfileSong.pk))
                # sorts the set by artists, anti-alphabetical ordering
                artist_za_set.sort(key=lambda tup: tup[0].lower(), reverse=True)
                # function to make list of displayable songs
                profile_songs = order_profile_songs(profile_artistsza, artist_za_set)
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
                # function to make list of displayable songs
                profile_songs = order_profile_songs(profile_showsaz, show_az_set)
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
                # function to make list of displayable songs
                profile_songs = order_profile_songs(profile_showsza, show_za_set)
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
            user_song_already_set = already(user_song_list, user_primary) # function already
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
                user_primary = request.user.pk
                user_song_already_set = already(user_song_list, user_primary) # function already
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