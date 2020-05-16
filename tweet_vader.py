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

    spark = SparkSession\
        .builder\
        .appName("TwitterSentimentAnalysis")\
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    tweetsDFRaw = spark.readStream\
                        .format("kafka")\
                        .option("kafka.bootstrap.servers", host + ":" + port)\
                        .option("subscribe", topic)\
                        .load()

    #tweetsDF = tweetsDFRaw.selectExpr("CAST(value AS STRING) as tweet")
    tweetsDF = tweetsDFRaw.selectExpr("split(value,',')[0] as tweet", "split(value,',')[1] as location",
                                      "split(value,',')[2] as timestamp")
    #print(tweetsDF.show())
    #tweetsDF[['tweet', 'location']] = tweetsDF.tweet.str.split(": location : ", expand=True, )
    #tweetsDF.withColumn("temp", split(col("tweet"), ": location : ")).select(col("*") +: (0 until 1).map(i= > col("temp").getItem(i).as(s"location")): _ *)

    analyser = SentimentIntensityAnalyzer()

    stop_words = list(set(stopwords.words('english')))

    def add_sentiment_score(tweet):
        #text = tweet.split(",")
        sentence = sent_tokenize(tweet)
        for i in sentence:
            i = re.sub(r'[^\w\s]', '', i)
            words = word_tokenize(i, "english", True)
            filtered = [w for w in words if not w in stop_words]
            score = analyser.polarity_scores(" ".join(filtered))
            print('Tweet: ' + str(tweet) + '\t' + 'Sentiment: ' + str(score))
            if score['compound'] > 0.0 and score['compound'] <= 1.0:
                return 'Positive'
            elif score['compound'] < 0.0 and score['compound'] >= -1.0:
                return 'Negative'
            elif score['compound'] == 0.0:
                return 'Neutral'

    add_sentiment_score_udf = udf(
                                add_sentiment_score,
                                StringType()
                                )

    tweetsDF = tweetsDF.withColumn(
                                    "sentiment_score",
                                    add_sentiment_score_udf(tweetsDF.tweet)
                                    )
    query = tweetsDF.writeStream\
                                .outputMode("append")\
                                .format("console")\
                                .option("truncate", "false")\
                                .trigger(processingTime="5 seconds")\
                                .start()\
                                .awaitTermination()
