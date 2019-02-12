import pandas as pd
import nltk
import stopwords
import re

class Song_Lyrics:
    def __init__(self, lyrics):
        self.all_tokens = self.tokenizeLyrics(lyrics)
        self.filtered_tokens = self.tokenizeLyrics(lyrics, True)
    
    def tokenizeLyrics(self, lyrics, include_stopwords=False):
        # Converting to lowercase and removing square brackets metadata
        edited = lyrics.replace(',','').lower()
        square_brackets_re = r'\[.*?\]'
        edited = re.sub(square_brackets_re, '', edited)
        final_token = nltk.WhitespaceTokenizer().tokenize(edited)

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
