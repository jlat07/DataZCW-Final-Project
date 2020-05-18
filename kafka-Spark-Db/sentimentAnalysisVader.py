from nltk.tokenize import word_tokenize, sent_tokenize
import re
import os
from nltk.corpus import stopwords
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
from wordcloud import WordCloud
from nltk.stem import PorterStemmer
from nltk.book import *
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyser = SentimentIntensityAnalyzer()


def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    if score['compound'] > 0.0 and score['compound'] <= 1.0:
        return 'Positive'
    elif score['compound'] < 0.0 and score['compound'] >= -1.0:
        return 'Negative'
    elif score['compound'] == 0.0:
        return 'Neutral'


def remove_punctuation(sentence):
    sentence = re.sub(r'[^\w\s]', '', sentence)
    return sentence


def remove_stopwords(sentence):
    return [w for w in sentence if not w in stop_words]


# d = dict()
stop_words = list(set(stopwords.words('english')))
id = 0
tweets = open('twitter_data_analysis2020-05-09-18.csv', 'r').readlines()
for tweet in tweets:
    try:
        id = id + 1
        text = tweet.split(",")
        sentence = sent_tokenize(text[2])
        for i in sentence:
            # remove_punctuation(i)
            words = word_tokenize(remove_punctuation(i), "english", True)
            filtered = remove_stopwords(words)
            print(sentiment_analyzer_scores(" ".join(filtered)))
            print('ID: ' + str(id) + '\t' + 'Tweet: ' + str(tweet) + '\t' + 'Sentiment: ' +
                  str(sentiment_analyzer_scores(" ".join(filtered))))

    except:
        continue
