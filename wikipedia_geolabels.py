import wikipedia
import pandas as pd
from geotext import GeoText

# This script uses wikipedia and geotext libraries to annotate a provided CSV containing search terms, 
# to identify whether the wikipedia entry found for the search term describes a newspaper or media entity,
# and based on the summary of the wikipedia entry, determine the associated city and country

def main():

	df = pd.read_csv("input.csv")

	wiki_url = []

	summary_city_col = []
	summary_country_col = []

	for (idx, row) in df.iterrows():

		name = row['Name']

		print ('Searching for ... ' + name)

		# search for associated wiki article
		try:
			summary = wikipedia.summary(name, sentences=5)

			# check if summary mentions one of the following news-related keywords
			if ('news' or 'television' or 'media' or 'publication' or 'magazine') in summary: 
				newspage = wikipedia.page(name)

				wiki_url.append(newspage.url)

				places = GeoText(summary)

				# extract place mentions from summary
				try:
					city = places.cities[0]
					summary_city_col.append(city)
				except:
					summary_city_col.append('')

				try:
					country = places.countries[0]
					summary_country_col.append(country)
				except:
					summary_country_col.append('')


			#if summary has no new-related mentions, decide it is not a valid article
			else:
				print ('News keyword not found')

				wiki_url.append('')

				summary_city_col.append('')
				summary_country_col.append('')

		# Disambiguation errors or no article found
		except:
			
			wiki_url.append('')

			summary_city_col.append('')
			summary_country_col.append('')


	df['wiki_url'] = wiki_url

	df['wiki_summary_city'] = summary_city_col
	df['wiki_summary_country'] = summary_country_col

	df.to_csv("output.csv")




if __name__ == "__main__":
	main()
