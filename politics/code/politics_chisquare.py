# N11 = day & republican
# N10 = day & not republican
# N00 = not day & not republican
# N01 = not day & republican

import csv
import re

handle_to_catlist = {}
categories = ["democrat", "republican", "liberal", "conservative", "libertarian"]
total_word_count = {}
person_count = dict([(category, 0) for category in categories])
handle_count = 0;

with open("../user_data_politics.csv", "rb") as f:
	reader = csv.reader(f)
	category_set = set(categories)
	for row in reader:
		handle_to_catlist[row[0].lower()] = list(set(row[3].split(", ")) & category_set)



word_counts = dict([(handle, {}) for handle in handle_to_catlist])
with open("../politicstweets_cleaned.csv", "rb") as f:
	reader = csv.reader(f)
	for row in reader:
		handle = row[0]
		if not handle: continue
		category_list = handle_to_catlist[handle.lower()]
		category_list = filter(lambda cat: cat in categories, category_list)
		if not category_list: continue
		for category in category_list:
			handle_count += 1
			person_count[category] += 1
		all_words = " ".join(row[1:]).split()
		words = filter(lambda word: not word.startswith("http") and "@" not in word and not word == "RT", all_words)
		words = map(lambda word: word.strip(".,!?';:+\"/><$@(){}-~[]&").lower(), words)
		for word in words:
			 for handle in handle_to_catlist:
			 	word_counts[handle].setdefault(word, 0)
				word_counts[handle][word] += 1
