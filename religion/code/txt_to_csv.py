import re
import csv

sep = "\n----------------------------------------------------------------------\n\n"
with open("../religiontweets_cleaned.txt", "r") as f:
	with open("../religiontweets_cleaned.csv", "wb") as out:
		writer = csv.writer(out)
		ftext = f.read()
		sections = ftext.split(sep)
		for section in sections:
			user_tweets = []
			handle = section.split(" - ", 1)[0]
			user_tweets.append(handle)
			user_tweets.extend(section.split(handle + " - ")[1:])
			writer.writerow(user_tweets)
