from django.contrib import admin
from .models import AotData, MySongUser

@admin.register(AotData)
class AotDataAdmin(admin.ModelAdmin):
    list_display = ('song', 'artist', 'show')
    ordering = ('pk',)

@admin.register(MySongUser)
class MySongUserAdmin(admin.ModelAdmin):
    display = 'MyUser'
    ordering = ('pk',)
    
