from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 
  
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
  
# Testing
tweets = {"Tweet1":"Zip code has the best Data Engineering students.",
        "Tweet2":"I am feeling blah today", 
        "Tweet3":"I am very sad today."}

def print_all(tweets: dict):
    for k, v in tweets.items():
        print(f"{k} is")
        sentiment_scores(v)
    

print_all(tweets)