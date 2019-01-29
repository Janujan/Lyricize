import pandas as pd
import nltk
from nltk.corpus import stopwords
import re

# Tokenizing types/words from lyrics (more preprocessing to be done)
# TO DO: tolowercase, remove stopwords, edge case punctuation handling
def tokenizeLyrics(lyrics, include_stopwords=False):

    # Converting to lowercase and removing square brackets metadata
    edited = lyrics.replace(',','').lower()
    square_brackets_re = r'\[.*?\]'
    edited = re.sub(square_brackets_re, '', edited)
    final_token = nltk.WhitespaceTokenizer().tokenize(edited)


    if (include_stopwords == True):
        # Removing filtered stopwords
        words_to_keep = ['only', 'myself','yourself','yourselves','most','again','while','down',
                        'himself', 'herself', 'which','ourselves','between','after','being','both',
                        'won', 'who', 'what','where','why','themselves','against','now','same',
                        'very','once','further','over','under','up','above','below','before']
        words_to_add = ["i'm","i'd","i'll","that's","he's","she's","they're","you're","we're"]
        stop_words = set(stopwords.words('english')).difference(words_to_keep)
        stop_words.update(words_to_add)
        final_token = [word for word in final_token if word not in stop_words]

    text = nltk.Text(final_token)
    return (text)

# Total word count (including 'Verse', 'Chorus')
def wordCount(lyrics):
    lyrics = tokenizeLyrics(lyrics)
    return (len(lyrics))

# Number of distinct words in track
def uniqueWordCount(lyrics):
    lyrics = tokenizeLyrics(lyrics)
    return (len(set(lyrics)))

# Percentage of words unique out of total words
def lexicalRichness(lyrics):
    lyrics = tokenizeLyrics(lyrics)
    return (str(len(set(lyrics))/len(lyrics) * 100) + '%')

# Percentage of one word over the track
def percentageOfTrack(word, lyrics):
    lyrics = tokenizeLyrics(lyrics)
    return (str(lyrics.count(word) / len(lyrics) * 100) + '%')

# Top 10 words and their count
def top10words(lyrics):
    lyrics = tokenizeLyrics(lyrics, True)
    fdist = nltk.FreqDist(lyrics)
    print(fdist)
    return(fdist.most_common(10))

# song = pd.read_json('Lyrics_TheWeeknd.json')
# lyrics = song['songs'][0]['lyrics']
# print(wordCount(lyrics))
# print(uniqueWordCount(lyrics))
# print(lexicalRichness(lyrics))
# print(percentageOfTrack('yeah',lyrics))
# print(top10words(lyrics))