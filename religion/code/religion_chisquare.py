# N11 = day & republican
# N10 = day & not republican
# N00 = not day & not republican
# N01 = not day & republican

import csv
import re

handle_to_catlist = {}
categories = ["christian", "christianity", "catholic", "judaism", "jewish", "muslim", "islam", "hindu", "hinduism", "atheist", "atheism"]
word_counts = dict([(category, {}) for category in categories])
total_word_count = {}
person_count = dict([(category, 0) for category in categories])

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
        # combine similar topics
        if "christian" in category_list and "christianity" not in category_list:
            category_list.append("christianity")
        if "jewish" in category_list and "judaism" not in category_list:
            category_list.append("judaism")
        if "muslim" in category_list and "islam" not in category_list:
            category_list.append("islam")
        if "atheist" in category_list and "atheism" not in category_list:
            category_list.append("atheism")
        for category in category_list:
            person_count[category] += 1
        all_words = " ".join(row[1:]).split()
        words = filter(lambda word: not word.startswith("http") and not word.startswith("@") and not word == "RT", all_words)
        words = map(lambda word: word.strip(".,!?';:+\"/><$@(){}-~[]&").lower(), words)
        for word in words:
            for category in category_list:
                word_counts[category].setdefault(word, 0)
                word_counts[category][word] += 1
            total_word_count.setdefault(word, 0)
            total_word_count[word] += 1

# new categories
categories = ["christianity", "catholic", "judaism", "islam", "hinduism", "atheism"]
total_words_by_category = {}
for category in categories:
    total_words_by_category[category] = sum(word_counts[category].values())

chi_sq_by_category = dict([(category, {}) for category in categories])
for word in total_word_count.keys():
    for category in categories:
        N11 = word_counts[category].get(word, 0)
        N10 = total_word_count[word] - N11
        N00 = sum([total_words_by_category[c] - word_counts[c].get(word, 0) for c in categories if c != category])
        N01 = total_words_by_category[category] - word_counts[category].get(word, 0)
        N = person_count[category]
        #N = N11 + N10 + N01 + N00
        chi_sq = 1.0*N*(N11*N00 - N10*N01)**2 / ((N11 + N01)*(N11 + N10)*(N10 + N00)*(N01 + N00))
        chi_sq_by_category[category][word] = chi_sq

with open("../religion_chisquare.csv", "wb") as f:
    writer = csv.writer(f)
    for category in categories:
        word_chi_list = list(reversed(sorted(list(chi_sq_by_category[category].iteritems()), key=lambda x: x[1])))[:1500]
        word_chi_cat = []
        for word, chi in word_chi_list:
            word_chi_cat.append([word, chi, category])
        writer.writerows(word_chi_cat)
