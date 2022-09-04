from django.db import models
from django.conf import settings

class AotData(models.Model):
    song = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    annid = models.IntegerField(blank=True)
    show = models.CharField(max_length=200)
    opedin = models.CharField(max_length=25)
    h720 = models.URLField(max_length=100, blank=True)
    h480 = models.URLField(max_length=100, blank=True)
    mp3 = models.URLField(max_length=100, blank=True)
    #foreign key to individual score
    #foreign key to global scorer


    def __str__(self):
        return """Song: %s | Artist: %s | annid: %s | Show: %s | Type: %s
        """%(self.song, self.artist, self.annid, self.show, self.opedin)


class MySongUser(models.Model):
    MyUser = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
    )
    my_songs = models.ManyToManyField(AotData, blank=True)

    def __str__(self):
        return "Username: %s"%(self.MyUser)


class SongScore(models.Model):
    #inherit 
    pass

