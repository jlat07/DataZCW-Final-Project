import re
import sys
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

if __name__ == "__main__":
    host = 'localhost'
    port = '9092'
    topic = 'tweet_stream'

    spark = SparkSession \
        .builder \
        .appName("TwitterSentimentAnalysis") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    tweetsDFRaw = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", host + ":" + port) \
        .option("subscribe", topic) \
        .load()

    tweetsDF = tweetsDFRaw.selectExpr("split(value,',')[0] as tweet", "split(value,',')[1] as location",
                                      "split(value,',')[2] as timestamp")

    analyser = SentimentIntensityAnalyzer()

    stop_words = list(set(stopwords.words('english')))


    def add_sentiment_score(tweet):
        # text = tweet.split(",")
        sentence = sent_tokenize(tweet)
        for i in sentence:
            i = re.sub(r'[^\w\s]', '', i)
            words = word_tokenize(i, "english", True)
            filtered = [w for w in words if not w in stop_words]
            score = analyser.polarity_scores(" ".join(filtered))
            print('Tweet: ' + str(tweet) + '\t' + 'Sentiment: ' + str(score))
            if 0.0 < score['compound'] <= 1.0:
                return 'Positive'
            elif 0.0 > score['compound'] >= -1.0:
                return 'Negative'
            elif score['compound'] == 0.0:
                return 'Neutral'

    def add_value(tweet,location,timestamp,score):
        return str(tweet) + "," + str(location) + "," + str(timestamp) + "," + str(score)


    add_sentiment_score_udf = udf(
        add_sentiment_score,
        StringType()
    )

    add_value_udf = udf(
        add_value,
        StringType()
    )

    tweetsDF = tweetsDF.withColumn(
        "sentiment_score",
        add_sentiment_score_udf(tweetsDF.tweet)
    )

    tweetsDF = tweetsDF.withColumn(
        "value",
        add_value_udf(tweetsDF.tweet,tweetsDF.location,tweetsDF.timestamp,tweetsDF.sentiment_score)
    )

    tweetsDFNew = tweetsDF.select("value")

    query = tweetsDFNew \
        .writeStream \
        .outputMode("append") \
        .format("kafka") \
        .option("kafka.bootstrap.servers", host + ":" + port) \
        .option("topic","tweet_sentiment_score")\
        .option("truncate", "false") \
        .option("checkpointLocation", "/Users/amishra/DEV/checkpoint")\
        .start() \
        .awaitTermination()

#.selectExpr("split(value,',')[0] as tweet", "split(value,',')[1] as location",
#            "split(value,',')[2] as timestamp", "split(value,',')[3] as sentiment_score")\
