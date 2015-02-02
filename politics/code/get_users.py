import mechanize
import re
import csv


class UserData:
	"""
	handle -- user's handle (prepended by @)
	name -- user's name
	bio -- user's bio
	"""
	def __init__(self, handle, name, bio, category, source):
		self.handle = handle
		self.name = name
		self.bio = bio
		self.category = category
		self.source = source

	def as_list(self):
		return [self.handle, self.name, self.bio, self.category, self.source]

	def __str__(self):
		", ".join(self.as_list())


# Creates the user objects from the
def generate_users():
	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	english_words = set([])
	with open("/usr/share/dict/words", "r") as f:
		for line in f:
			line = line.strip()
			english_words.add(line)
	source_list = ["http://twellow.com", "http://tweepz.com", "http://wefollow.com/"]
	category_list = ["politics", "democrat", "republican", "liberal", "conservative", "libertarian"]
	user_list = {}
	for source in source_list:
		if source == source_list[0]:
			# Regexes to extract Twitter handles, user names, and bios from page
			handle_regex = re.compile(r"\((@\w+)\)")
			name_regex = re.compile(r"<a href=\"/[^\"]+\">([^<]+)<")
			bio_regex = re.compile(r"</div>\s*(.*?)\s*</div>\s*<div class=\"clear\">&nbsp;</div>", re.DOTALL)
		elif source == source_list[1]:
			# Regexes to extract Twitter handles, user names, and bios from page
			handle_regex = re.compile(r"\((@\w+)\)")
			name_regex = re.compile(r"<a class=\"reslink\" href=\"[^\"]+\">([^<]+)<")
			bio_regex = re.compile(r"<em style=\"color:#777777\">(.*?)</em>", re.DOTALL)
		elif source == source_list[2]:
			# Regexes to extract Twitter handles, user names, and bios from page
			handle_regex = re.compile(r"target=\"_blank\">(.*?)</a>")
			name_regex = re.compile(r"<p class=\"user-name\"><a href=\"[^\"]+\">([^<]+)<")
			bio_regex = re.compile(r"<p class=\"user-bio\">\s*(.*?)\s*</p>", re.DOTALL)
		for category in category_list:
			for pg in (xrange(1, 20)):
				user_added = 0;

				# TWELLOW
				if source == source_list[0]:
					# Paginates through the Politics category
					response = br.open("http://twellow.com/categories/%s?p=%d" % (category, pg))
					page_source = response.read()
					# User entry delimiter
					delimiter = """<div class="search-cat-user-name">"""

				# TWEEPZ #1
				elif source == source_list[1]:
					# Paginates through the Politics category
					response = br.open("http://tweepz.com/search?q=%s&followers=10000&p=%d" % (category, pg))
					page_source = response.read()
					# User entry delimiter
					delimiter = """<div class="span7">"""

				# TWEEPZ #2
				elif source == source_list[1]:
					# Paginates through the Politics category
					response = br.open("http://tweepz.com/search?q=%s&followers=5000-10000&p=%d" % (category, pg))
					page_source = response.read()
					# User entry delimiter
					delimiter = """<div class="span7">"""

				# TWEEPZ #3
				elif source == source_list[1]:
					# Paginates through the Politics category
					response = br.open("http://tweepz.com/search?q=%s&followers=2000-5000&p=%d" % (category, pg))
					page_source = response.read()
					# User entry delimiter
					delimiter = """<div class="span7">"""

				# WEFOLLOW
				elif source == source_list[2]:
					# Paginates through the Politics category
					if pg == 1:
						response = br.open("http://wefollow.com/interest/%s/50-100/" % (category))
					else:
						response = br.open("http://wefollow.com/interest/%s/50-100/page%d" % (category, pg))
					page_source = response.read()
					# User entry delimiter
					delimiter = """<div class="user-info">"""

				for entry in page_source.split(delimiter)[1:]:
					user_added = 1;
					# Generates a user object using the regexes
					handle = handle_regex.findall(entry)[0]
					name = name_regex.findall(entry)[0]
					ret = bio_regex.findall(entry)
					# case where there is a bio
					if ret:
						bio = ret[0]
					else:
						bio = ""
					# case where bio has < 60% english words
					i = 0
					j = 0
					for word in re.split('\\W+', bio):
						if not word:
							continue
						if word in english_words:
							i+=1
						j+=1
					if len(bio) > 7 and not j:
						continue
					if j and 1.0 * i/j < 0.7:
						continue
					# check for duplicate handles
					if handle in user_list:
						obj = user_list[handle]
						if obj.category != category:
							obj.category = ", ".join((obj.category, category))
						if obj.source != source:
							obj.source = ", ".join((obj.source, source))
					else:
						user = UserData(handle, name, bio, category, source)
						user_list[handle] = user
				if user_added != 1:
					break
	return user_list

def dump_users(user_list):
	with open("../udp.csv", "wb") as f:
		writer = csv.writer(f)
		for user in user_list.values():
			writer.writerow(user.as_list())


if __name__ == "__main__":
	dump_users(generate_users())
