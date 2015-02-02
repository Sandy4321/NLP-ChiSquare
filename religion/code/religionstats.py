import csv
import re

handle_to_catlist = {}
categories = ["christian", "christianity", "catholic", "judaism", "jewish", "muslim", "islam", "hindu", "hinduism", "atheist", "atheism"]
word_counts = dict([(category, {}) for category in categories])
total_word_count = {}
person_count = dict([(category, 0) for category in categories])
tweets_count = dict([(category, 0) for category in categories])
people = 0

with open("../user_data_religion.csv", "rb") as f:
  reader = csv.reader(f)
  category_set = set(categories)
  for row in reader:
    handle_to_catlist[row[0].lower()] = list(set(row[3].split(", ")) & category_set)

with open("../religiontweets_cleaned.csv", "rb") as f:
  reader = csv.reader(f)
  for row in reader:
    handle = row[0]
    if not handle: continue
    category_list = handle_to_catlist[handle.lower()]
    category_list = filter(lambda cat: cat in categories, category_list)
    if not category_list: continue
    if "christian" in category_list and "christianity" not in category_list:
        category_list.append("christianity")
    if "jewish" in category_list and "judaism" not in category_list:
        category_list.append("judaism")
    if "muslim" in category_list and "islam" not in category_list:
        category_list.append("islam")
    if "atheist" in category_list and "atheism" not in category_list:
        category_list.append("atheism")
    num_tweets = (len(row) - 1)
    people += 1
    for category in category_list:
      person_count[category] += 1
      tweets_count[category] += num_tweets

categories = ["christianity", "catholic", "judaism", "islam", "hinduism", "atheism"]
total_tweets = 0;
for category in tweets_count:
    total_tweets += tweets_count[category]

print "Total number of people: ", people
print "Total number of tweets in religion: ", total_tweets
for category in categories:
    print "People in " , category, ": ",  person_count[category]
    print "Tweets in" , category, ": ", tweets_count[category]
