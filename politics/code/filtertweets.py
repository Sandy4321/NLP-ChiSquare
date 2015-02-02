# Remove users whose tweets are in foreign languages/consist mostly of unknown characters
import re

english_words = set([])
with open("/usr/share/dict/words", "r") as f:
	for line in f:
		line = line.strip()
		english_words.add(line)

sep = "\n----------------------------------------------------------------------\n\n"
with open("../udp.txt", "r") as f:
	with open("politicstweets_cleaned.txt", "w") as out:
		ftext = f.read()
		sections = ftext.split(sep)
		for section in sections:
			handle = section.split(" - ", 1)[0]
			new_section = []
			for line in section.splitlines():
				if line.startswith(handle):
					line = line.split(" ", 2)[-1]
				new_section.append(line)
			new_section = " ".join(new_section)
			if not new_section:
				continue
			words = filter(lambda word: not word.startswith("@") and not word.startswith("#") and not word.startswith("http:") and not word == "RT", new_section.split())
			words = map(lambda word: word.strip(".!?';:\"()").lower(), words)
			ratio = 1.0*sum(map(lambda x: x in english_words, words)) / len(words)
			if ratio < .40:
				print handle, "\t\t", ratio
			else:
				out.write(section)
				out.write(sep)
