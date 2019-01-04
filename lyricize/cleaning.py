import pandas as pd

# Clean Lyrics
def tempCleaner(jsonFile):
    lyrics = jsonFile['songs'][0]['lyrics']
    return (lyrics.splitlines())

# Line Count
def lineCount(lyrics):
    return(len(lyrics))

# Main
artistFile = pd.read_json('Lyrics_Drake.json')
lyrics = tempCleaner(artistFile)
print(lineCount(lyrics))