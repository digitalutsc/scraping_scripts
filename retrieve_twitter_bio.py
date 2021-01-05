import pandas as pd
import tweepy

# Based on the provided twitter handles in a CSV, this script populates a new column twitter_bio 
# with their user description. A consumer Twitter API key is needed to authenticate to Twitter.

def scrape_twitter_bio(twitter_handle, api):

	# Retrieve the User object for a given twitter handle
	user = api.get_user(twitter_handle)
	bio = user.description
	return bio


def main():

	source_df = pd.read_csv("input.csv")
	
	# Authenticate to Twitter
	auth = tweepy.OAuthHandler("YOUR_CONSUMER_KEY", "YOUR_CONSUMER_SECRET")
	auth.set_access_token("YOUR_CONSUMER_KEY", "YOUR_CONSUMER_SECRET")

	api = tweepy.API(auth)	

	twitter_bio = []

	for (idx, row) in source_df.iterrows():

		handle = row['Source']
		print ('Searching for user ... ' + handle)

		try:
			scraped_bio = scrape_twitter_bio(handle, api)
			twitter_bio.append(scraped_bio)

		except:

			twitter_bio.append('')

	source_df['twitter_bio'] = twitter_bio

	source_df.to_csv("output.csv")


if __name__ == "__main__":
	main()
