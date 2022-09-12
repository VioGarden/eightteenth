from django.contrib import admin
from .models import AotData, MySongUser, UserList, SongScore

@admin.register(AotData)
class AotDataAdmin(admin.ModelAdmin):
    list_display = ('song', 'artist', 'show')
    ordering = ('pk',)

@admin.register(MySongUser)
class MySongUserAdmin(admin.ModelAdmin):
    display = 'MyUser'
    ordering = ('pk',)

@admin.register(UserList)
class UserListAdmin(admin.ModelAdmin):
    display = 'ProfileUser'
    ordering = ('pk',)

@admin.register(SongScore)
class SongScoreAdmin(admin.ModelAdmin):
    display = 'PossibleScore'
    ordering = ('pk',)
    
