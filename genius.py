
import lyricsgenius as genius
import json

access_token ="H8gi1tgFffzZjO9PRxMNly8l04APCJHQNodtzCRGs_bIweR0x5JvhT7h6dq1-kED"

api = genius.Genius(access_token)
artist = api.search_artist("Drake", max_songs=3, sort='popularity', get_full_info=True)

#get_full_info to false speeds up search considerably, you drop annotations
# can sort on popularity or title
# Max songs to none is all songs

#save_lyrics saves a json file unfortunately, need to find a way to stop that
#OR just delete after each run
data = artist.save_lyrics(overwrite=True)

#json tags of d:
# songs, title, album, year, lyrics
# after that its just a bunch of annotations
extract = data['songs'][0]['year']
print(extract)


extract = data['songs'][0]['album']
print(extract)

extract = data['songs'][0]['title']
print(extract)

extract = data['songs'][0]['lyrics']
print(extract)

artist_name = data['artist']
print(artist_name)
