
from wordcloud import WordCloud 
import matplotlib.pyplot as plt 
import csv 

# file object is created 
file_ob = open(r"/Users/jthompson/dev/DataZCW-Final-Project/Data/twitter_data_analysis2020-05-09-18.csv") 

# reader object is created 
reader_ob = csv.reader(file_ob) 

# contents of reader object is stored . 
# data is stored in list of list format. 
reader_contents = list(reader_ob) 

# empty string is declare 
text = "" 

# iterating through list of rows 
for row in reader_contents : 
	
	# iterating through words in the row 
	for word in row : 

		# concatenate the words 
		text = text + " " + word 

# stopwords = set(STOPWORDS)
stopwords =set(["https", "the","for", "co", "south africa", "SouthAfrica", "more", "than", "has", "been", "to"])

wordcloud = WordCloud(width=480, height=480,
			max_words = 200,
			stopwords= stopwords).generate(text) 

# plot the WordCloud image 
plt.figure() 
plt.imshow(wordcloud, interpolation="bilinear") 
plt.axis("off") 
plt.margins(x=0, y=0) 
plt.show() 

