import pandas as pd
import nltk
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from django.http import HttpResponse
import io
from wordcloud import WordCloud

class Song_Lyrics:
    def __init__(self, lyrics):
        # Converting to lowercase and removing square brackets metadata
        edited = lyrics.replace(',','').lower()
        square_brackets_re = r'\[.*?\]'    
        self.lyrics = re.sub(square_brackets_re, '', edited)
        self.all_tokens = self.tokenizeLyrics(self.lyrics)
        self.filtered_tokens = self.tokenizeLyrics(lyrics, True)
    
    def tokenizeLyrics(self, lyrics, include_stopwords=False):
        final_token = nltk.WhitespaceTokenizer().tokenize(lyrics)

        if (include_stopwords == True):
            # Removing filtered stopwords
            custom_stopwords = nltk.data.load('stopwords/english', format="raw")
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
    
    # Wordcloud generation
    def wordcloud(self):
        wordcloud = WordCloud(background_color = 'black',
        # stopwords = nltk.data.load('stopwords/english', format="raw")
        ).generate(str(self.lyrics))
        fig = plt.figure(facecolor = 'k', edgecolor = 'k')
        plt.imshow(wordcloud, interpolation = 'bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        response = HttpResponse(buf.getvalue(), content_type='image/png')
        return (response)
        