import time, requests


APIKEY = ".."
HASHTAG = ""

print("Starting DEMO app..")
while True:
  for tweet in check_for_relevant_tweets():
    process_tweet(tweet)
  time.sleep(10)
    
