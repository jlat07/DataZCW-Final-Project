import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from afinn import Afinn

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

    tweetsDF = tweetsDFRaw.selectExpr("CAST(value AS STRING) as tweet")
    tweetsDF[['tweet', 'location']] = tweetsDF.Name.str.split(": location : ", expand=True, )

    afinn = Afinn()

    def add_sentiment_score(text):

        sentiment_score = afinn.score(text)
        return sentiment_score

    add_sentiment_score_udf = udf(
                                add_sentiment_score,
                                FloatType()
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



