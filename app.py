
from tweepy.auth import OAuthHandler 
import tweepy, json, re, sys

consumer_key = ''
consumer_secret = ''

access_token = ''
access_secret = ''

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

number_tweets_to_get = 20

api = tweepy.API(auth)

#cleans up tweets using regex
def clean_tweet(orig_tweet):
    cleanTweet = re.sub(r'https[^\s]+', '', orig_tweet)
    cleanTweet = re.sub(r'[^\w\s]', '', cleanTweet)
    return cleanTweet


def main():

	#results = tweepy.Cursor(api.search, q='', lang='en').items(number_tweets_to_get)
	results = tweepy.Cursor(api.user_timeline, screen_name=sys.argv[1]).items(number_tweets_to_get)
	
	with open("uncleanedtweets.txt", "w") as unclean_file, open("tweets.txt", "w") as clean_file:
		 for tweet in results:
		    tweet.text = tweet.text.encode('utf-8') #encode the string properly
		    unclean_file.write(tweet.text + '\n')   #unclean text file   
		    clean_text = clean_tweet(tweet.text)
		    clean_file.write(clean_text + '\n')     #clean text file
		    
		    #Exclude all retweets
		    if (not tweet.retweeted) and ('RT @' not in tweet.text):
		        print(clean_text)
			    

if __name__ == "__main__":
	main()



