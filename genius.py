
import lyricsgenius as genius
import json

client_id = "QDLq4h4n98Jlq9AoFOSqbW6ESGVCId5j4HDCZ3fkrNiFu9s_R89PjhojrqrB_IOi"

client_secret = "mwiQX_N4dgd813ulAJJE4_lhRSCpWM0cM6APJgM03pZHx84NdVz5F4bpTVOuSp3TfZpma4cTyw2ZpMzNl3_1Sg"

access_token ="H8gi1tgFffzZjO9PRxMNly8l04APCJHQNodtzCRGs_bIweR0x5JvhT7h6dq1-kED"

api = genius.Genius(access_token)
artist = api.search_artist("Drake", max_songs=3, sort='popularity', get_full_info=False)

#get_full_info to false speeds up search considerably, you drop annotations
# can sort on popularity or title
# Max songs to none is all songs

#save_lyrics saves a json file unfortunately, need to find a way to stop that
#OR just delete after each run
data = artist.save_lyrics(overwrite=False)

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
