from django.db import models

# Create your models here.
class Artist(models.Model):
    artist_name = models.CharField(max_length=100)


    def __str__(self):
        return self.artist_name

    def __repr__(self):
        return self.artist_name
