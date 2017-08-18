
from tweepy.auth import OAuthHandler 
import tweepy, json, re, sys
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

consumer_key = 'o5NlxtXwBBgokHJcgRf8GmYwD'
consumer_secret = 'HaoS6xelrosLg8rSEFI7g10c8eWXicwYSNDvMZZrxR2q0b4VEw'

access_token = '894354910074089474-Uk9ksmyi11N1wmvc605KuZFUaR7hTWY'
access_secret = 'Mv9XxRjDYohH4YIeCV82biNnKcFxGWj2nEq4SxXl5wD7P'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

number_tweets_to_get = 20

api = tweepy.API(auth)

#cleans up tweets using regex and nltk
def clean_tweet(orig_tweet):
	#use regex to remove punctuation, numbers, https, etc.
    cleanTweet = re.sub(r'https[^\s]+', '', orig_tweet)
    cleanTweet = re.sub(r'[^\w\s]', '', cleanTweet)
    cleanTweet = cleanTweet.lower()
    
    #remove stop words from nltk library
    cachedStopWords = stopwords.words("english")
    cleanTweet= ' '.join([word for word in cleanTweet.split() if word not in cachedStopWords])
    cleanTweet = ''.join(str(x) for x in cleanTweet)
    return cleanTweet

#grabs and puts clean and uncleaned tweets in files    
def grabTweets(results):
	with open("uncleanedtweets.txt", "w") as unclean_file, open("tweets.txt", "w") as clean_file:
		 for tweet in results:
		    tweet.text = tweet.text.encode('utf-8') #encode the string properly
		    unclean_file.write('tweet: ' + tweet.text + '\n')   #create unclean text file   
		    clean_text = clean_tweet(tweet.text)
		    clean_file.write(clean_text + '\n')     #create clean text file
		    
		    #Exclude all retweets
		    # if (not tweet.retweeted) and ('RT @' not in tweet.text):
		    #     print(clean_text)
	
#count positive words in a single cleaned tweet		  
def countPositiveWords():
	#split all tweets into a list of words
	lines = open('tweets.txt', 'rb').readlines()
	positiveWords = set(line.strip() for line in open('positiveW.txt'))
	
	#find matches of positive words in the tweet
	for line in lines:
		words = line.split()
		count = 0
		for word in words:
			if word in positiveWords:
				count+=1
		print count
			
		  
		        
def main():
	results = tweepy.Cursor(api.user_timeline, screen_name=sys.argv[1]).items(number_tweets_to_get)
	grabTweets(results);
	countPositiveWords()

	
	# 	# The search term you want to find
	# query = "@realDonaldTrump"
	# # Language code (follows ISO 639-1 standards)
	# language = "en"
	
	# # Calling the user_timeline function with our parameters
	# results = api.search(q=query, lang=language)
	
	# # foreach through all tweets pulled
	# for tweet in results:
	#   # printing the text stored inside the tweet object
	#   print tweet.user.screen_name,"Tweeted:",tweet.text

if __name__ == "__main__":
	main()



