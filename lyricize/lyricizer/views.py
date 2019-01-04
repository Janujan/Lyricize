from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SearchForm
from .models import Artist
import lyricsgenius as genius
from cleaning import tempCleaner, lineCount

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
            return redirect('results')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm()

    return render(request, 'searchPage.html', {'form': form})


def results(request):

    artists = Artist.objects.all()
    print(artists)
    only_artist = artists[0]

    message = only_artist.artist_name
    print(only_artist)

    access_token ="H8gi1tgFffzZjO9PRxMNly8l04APCJHQNodtzCRGs_bIweR0x5JvhT7h6dq1-kED"

    api = genius.Genius(access_token)
    artist = api.search_artist(only_artist.artist_name, max_songs=1, sort='popularity', get_full_info=True)

    #overwrite to avoid prompt, add filename and location to delete later
    data = artist.save_lyrics(overwrite=True)

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

    artist_name = data['artist']
    print(artist_name)

    music = Music(only_artist.artist_name)
    music.year = year
    music.album = album
    music.title = title

    #line count:
    lyrics = tempCleaner(data)
    l_count = lineCount(lyrics)

    context = {
        "music" : music,
        "line_count": l_count
    }


    return render(request, 'resultsPage.html', context)
