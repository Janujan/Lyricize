import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk_data import stopwords
import re
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

# Modify NLTK Path to Director
nltk.data.path.append('nltk_data')

class Song:
    def __init__(self, lyrics, title, artist_name):
        # Converting to lowercase and removing square brackets metadata
        edited = lyrics.replace(',','').lower()
        square_brackets_re = r'\[.*?\]'
        self.lyrics = re.sub(square_brackets_re, '', edited)
        self.all_tokens = self.tokenizeLyrics(lyrics)
        self.filtered_tokens = self.tokenizeLyrics(lyrics, True)
        self.title = title
        self.artist_name = artist_name
    
    def tokenizeLyrics(self, lyrics, include_stopwords=False):
        final_token = nltk.WhitespaceTokenizer().tokenize(self.lyrics)

        if (include_stopwords == True):
            custom_stopwords = nltk.data.load('stopwords/english', format="raw")
            # Removing filtered stopwords
            words_to_keep = ['only', 'myself','yourself','yourselves','most','again','while','down',
                            'himself', 'herself', 'which','ourselves','between','after','being','both',
                            'won', 'who', 'what','where','why','themselves','against','now','same',
                            'very','once','further','over','under','up','above','below','before']
            words_to_add = ["i'm","i'd","i'll","that's","he's","she's","they're","you're","we're"]
            stop_words = set(custom_stopwords).difference(words_to_keep)
            stop_words.update(words_to_add)
            final_token = [word for word in final_token if word not in stop_words]

        text = nltk.Text(final_token)
        return (text)

    # Total word count
    def wordCount(self):
        return (len(self.all_tokens))

    def filteredWordCount(self):
        return (len(self.filtered_tokens))

    # Number of distinct words in track
    def uniqueWordCount(self):
        return (len(set(self.all_tokens)))

    # Percentage of words unique out of total words
    def lexicalRichness(self):
        return (len(set(self.all_tokens))/len(self.all_tokens) * 100)

    # Percentage of one word over the track
    def percentageOfTrack(self, word):
        return (self.all_tokens.count(word) / len(self.all_tokens) * 100)

    # Top 10 words and their count
    def top10words(self):
        fdist = nltk.FreqDist(self.filtered_tokens).most_common(10)
        most_common_dict = {}
        for words in range(len(fdist)):
            most_common_dict[fdist[words][0]] = fdist[words][1]
        return (most_common_dict)

    def audioFeatures(self):
        # Setting up Spotify credentials
        client_credentials_manager = SpotifyClientCredentials()
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        sp.trace=False

        #search for a song named 'title + artist' from Genius, in Spotify
        results = sp.search(q=self.title + ' ' + self.artist_name, limit=1)
        audio_features = {}

        #if no song was found in Spotify, output the song name that was read in and empty fields
        if not results['tracks']['items']:
            audio_features = {
                                'popularity': 0,
                                'energy': 0,
                                'dance': 0,
                                'liveness': 0,
                                'valence': 0,
                                'tempo': 0,
                                'instrumental': 0,
                                'acoustic': 0,
                                'artistName': 0
            }
        #if song was found on Spotify
        else:
            #Find the track's ID to get audio features
            track_id = results['tracks']['items'][0]['uri']
            
            #Get audio features using the track's ID stored in track_id
            features = sp.audio_features(track_id)
            
            if features[0] is not None:
                #define each variable needed from the "get audio features" "search for a track" query for the project
                audio_features = {
                                    'popularity': results['tracks']['items'][0]['popularity'],
                                    'energy': features[0]['energy'],
                                    'dance': features[0]['danceability'],
                                    'liveness': features[0]['liveness'],
                                    'valence': features[0]['valence'],
                                    'tempo': features[0]['tempo'],
                                    'instrumental': features[0]['instrumentalness'],
                                    'acoustic': features[0]['acousticness']
                }  
        # print(results['tracks']['items'][0]['name']+ ' ' + results['tracks']['items'][0]['artists'][0]['name'])
        return(audio_features)
        
    def sentiment_analysis(self):
        sentences = self.lyrics.splitlines()
        num_positive = 0
        num_negative = 0
        num_neutral = 0
        
        for sentence in sentences:
            sid = SentimentIntensityAnalyzer()
            comp = sid.polarity_scores(sentence)
            comp = comp['compound']
            if comp >= 0.5:
                num_positive += 1
            elif comp > -0.5 and comp < 0.5:
                num_neutral += 1
            else:
                num_negative += 1
        
        num_total = num_negative + num_neutral + num_positive
        percent_negative = (num_negative/float(num_total))*100
        percent_neutral = (num_neutral/float(num_total))*100
        percent_positive = (num_positive/float(num_total))*100

        return ({'positive': percent_positive, 
                 'neutral': percent_neutral,
                 'negative': percent_negative})
