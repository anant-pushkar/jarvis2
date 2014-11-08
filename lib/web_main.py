import urlparse
import re
from google import search
from DrakSuggestionsFetcher import *
 
if __name__ == "__main__":
	so = DrakStackOverflowStackApp()
	au = DrakAskUbuntuStackApp()
	ask=raw_input("Enter key to be searched: ")
	stackoverflow_query = ask + " stackoverflow"
	askubuntu_query = ask + " askubuntu"
	suggestions = []
	question_ids = []
	for url in search(stackoverflow_query, tld='es', lang='en', stop=20):
		hostname = urlparse.urlparse(url).hostname
		if(hostname == "stackoverflow.com"):
			path = urlparse.urlsplit(url).path
			pathx = str(path).split('/')
			question_ids.append(pathx[2])

	suggestions.extend(so.get_suggestions(question_ids))

	question_ids = []
	for url in search(askubuntu_query, tld='es', lang='en', stop=20):
		hostname = urlparse.urlparse(url).hostname
		if(hostname == "askubuntu.com"):
			path = urlparse.urlsplit(url).path
			pathx = str(path).split('/')
			question_ids.append(pathx[2])
	suggestions.extend(au.get_suggestions(question_ids))

	for suggestion in suggestions:
		print suggestion.codes
		print suggestion.confidence
		print "+++++++++++++++"
