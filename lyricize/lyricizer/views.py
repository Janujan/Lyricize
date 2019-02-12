from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SearchForm
from .models import Artist
import lyricsgenius as genius
#from cleaning import tempCleaner, lineCount
from summary import *
import nltk

class Music:
    def __init__(self,name):
        self.artist_name = name
        self.year = ''
        self.title = ''
        self.album = ''

def search(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            name = form.cleaned_data['artist_name']
            name.upper()
            #check if name already exists
            artists = Artist.objects.filter(artist_name = name)
            if not artists:
                form.save()

            print(name)
            #return redirect('results')
            return redirect('results' ,  artist_name = name )


    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm()

    return render(request, 'searchPage.html', {'form': form})


def results(request, artist_name):

    only_artist = artist_name
    print(only_artist)

    access_token ="H8gi1tgFffzZjO9PRxMNly8l04APCJHQNodtzCRGs_bIweR0x5JvhT7h6dq1-kED"

    api = genius.Genius(access_token)
    artist = api.search_artist(only_artist, max_songs=1, sort='popularity', get_full_info=True)

    #if artist doesnt exist, remove from database and go back to search page
    if artist is None:
        return_artist = Artist.objects.get(artist_name=only_artist)
        return_artist.delete()
        return redirect('search')

    #overwrite to avoid prompt, add filename and location to delete later
    data = artist.save_lyrics(overwrite=True)

    image_url = data['songs'][0]['image']
    print(data['songs'][0]['image'])

    #json tags of d:
    # songs, title, album, year, lyrics
    # after that its just a bunch of annotations
    year = data['songs'][0]['year']
    print(year)

    album = data['songs'][0]['album']
    print(album)

    title = data['songs'][0]['title']
    print(title)

    lyrics = data['songs'][0]['lyrics']
    #print(lyrics)

    print(artist_name)

    music = Music(only_artist)
    music.year = year
    music.album = album
    music.title = title

    #song object
    track_lyrics = Song_Lyrics(lyrics)

    context = {
        "music" : music,
        "word_count": track_lyrics.wordCount(),
        "lexical_richness": str(track_lyrics.lexicalRichness())[:4] + '%',
        "unique_count": track_lyrics.uniqueWordCount(),
        "image_url": image_url,
    }

    return render(request, 'resultsPage.html', context)
