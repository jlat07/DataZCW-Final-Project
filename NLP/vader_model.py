from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv 
  
# function to print sentiments 
# of the tweet. 
def sentiment_scores(tweet): 
  
    # Create a SentimentIntensityAnalyzer object. 
    sid_obj = SentimentIntensityAnalyzer() 
  
    # polarity_scores method of SentimentIntensityAnalyzer 
    # oject gives a sentiment dictionary. 
    # which contains pos, neg, neu, and compound scores. 
    sentiment_dict = sid_obj.polarity_scores(tweet) 
      

    print(sentiment_dict['neg']*100, "% Negative,") 
    print(sentiment_dict['neu']*100, "% Neutral,") 
    print(sentiment_dict['pos']*100, "% Positive,") 
  
    print("Overall Rated As", end = " ") 
  
    # decide sentiment as positive, negative and neutral 
    if sentiment_dict['compound'] >= 0.05 : 
        print("Positive") 
  
    elif sentiment_dict['compound'] <= - 0.05 : 
        print("Negative") 
  
    else : 
        print("Neutral") 
  
# Testing Sentiment
tweets = {"Tweet1":"Zip code has the best Data Engineering students.",
        "Tweet2":"I am feeling blah today", 
        "Tweet3":"I am very sad today."}

def print_all(tweets: dict):
    for k, v in tweets.items():
        print(f"{k} is")
        sentiment_scores(v)
    

# print_all(tweets)

# file object is created 
data = open(r"/Users/jthompson/dev/DataZCW-Final-Project/Data/twitter_data_analysis2020-05-09-18.csv") 

# reader object is created 
reader_ob = csv.reader(data) 

# contents of reader object is stored . 
# data is stored in list of list format. 
reader_contents = list(reader_ob) 
# print(reader_contents)
# empty string is declare 
text = "" 

# iterating through list of rows 
for row in reader_contents : 
	
	# iterating through words in the row 
	for word in row : 

		# concatenate the words 
		text = text + " " + word 


for row in reader_ob:
    for column in row:
        # prin(column)
        if column=="column 3":
            print(row)
            
