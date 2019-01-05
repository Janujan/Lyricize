import nltk

# Tokenizing types/words from lyrics (more preprocessing to be done)
# TO DO: tolowercase, remove stopwords, edge case punctuation handling
def tokenizeLyrics(lyrics):
    edited = lyrics.replace(',','')
    token = nltk.WhitespaceTokenizer().tokenize(edited)
    text = nltk.Text(token)
    return (text)

# Total word count (including 'Verse', 'Chorus')
def wordCount(lyrics):
    return (len(lyrics))

# Number of distinct words in track
def uniqueWordCount(lyrics):
    return (len(set(lyrics)))

# Percentage of words unique out of total words
def lexicalRichness(lyrics):
    return (str(len(set(lyrics))/len(lyrics) * 100) + '%')

# Percentage of one word over the track
def percentageOfTrack(word, lyrics):
    return (str(lyrics.count(word) / len(lyrics) * 100) + '%')

# Top 10 words and their count
def top10words(lyrics):
    fdist = nltk.FreqDist(lyrics)
    print(fdist)
    return(fdist.most_common(10))

# song = pd.read_json('Lyrics_TheWeeknd.json')
# lyrics = song['songs'][0]['lyrics']
# nltkText = tokenizeLyrics(lyrics)
# print(wordCount(nltkText))
# print(uniqueWordCount(nltkText))
# print(lexicalRichness(nltkText))
# print(percentageOfTrack('yeah',nltkText))
# print(top10words(nltkText))