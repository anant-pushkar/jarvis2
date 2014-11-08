import sys
sys.path.append('.')
import stackexchange
import codecs
import unicodedata
from xml.dom import minidom
import math
from xml.parsers.expat import ExpatError
import urlparse
import re
from google import search
import utils

search_keywords = ["pip", "install", "apt-get", "update", "dpkg", "easy_install"]

class DrakSuggestion:
	def __init__(self, text, codes, score, ticked, match_count):
		self.text = text
		self.codes = codes
		self.score = score
		self.confidence = 0
		self.is_ticked = ticked
		self.match_count = match_count
		self.keyword_confidence = 0
class DrakAbstractStackApp():
	def __init__(self):
		pass
	def get_suggestions(self, questionIds):
		questionIds = [x for x in questionIds if x.isdigit()]

		questions = self.site.questions(questionIds)
		suggestions = []
		
		index = 0
		for question in questions:
			questions_weight = math.exp(-1*0.1*index)
			suggestions_for_question = self.get_suggestions_for_question(question)
			max_score_of_suggestions_for_question = 0
			
			max_match_count_for_question = 0
			
			for suggest in suggestions_for_question:
				if max_score_of_suggestions_for_question < suggest.score:
					max_score_of_suggestions_for_question = suggest.score
				if suggest.match_count > max_match_count_for_question:
					max_match_count_for_question = suggest.match_count
			for suggest in suggestions_for_question:
				value_of_answer = suggest.score*1.0/(max_score_of_suggestions_for_question+0.01)
				self.calculate_confidence_of_suggestion(suggest, value_of_answer, questions_weight, max_match_count_for_question)
			suggestions.extend(suggestions_for_question)
			index = index+1
		return suggestions
		
	def get_suggestions_for_question(self, question):
		suggestions = []
		for answer in question.answers:
			text = ''
			codes = []
			try:
				xmldoc = minidom.parseString(self.get_xml_for_answer_body(answer).encode('utf-8'))
				for pNode in xmldoc.getElementsByTagName('p'):
					text = text + self.extract_text_from_node(pNode)
				for code in xmldoc.getElementsByTagName('code'):
					codes.append(self.extract_text_from_node(code))
				suggestions.append(DrakSuggestion(text, codes, self.get_upvotes(answer), self.is_ticked(answer), self.get_match_count(codes)))
			except AttributeError:
				pass#print "Attribute Error"
			except ExpatError:
				pass#print "Expat Error"
		return suggestions	

	def calculate_confidence_of_suggestion(self, suggest, value_of_answer, questions_weight, max_match_count_for_question):
		if(suggest.is_ticked == True):
			suggest.confidence = 40
		else:
			suggest.confidence = 30
				
		suggest.confidence = suggest.confidence + value_of_answer*30
		if len(suggest.codes) > 0:
			suggest.confidence = suggest.confidence + (1.0*suggest.match_count/(max_match_count_for_question+0.01))*30 
		suggest.confidence = suggest.confidence * questions_weight


	def get_match_count(self, codes):
		match_count = 0
		for code in codes:
			for keyword in search_keywords:
				if code.find(keyword):
					match_count = match_count + 1
					break
		return match_count	
			
			
	def get_upvotes(self, answer):
		return answer.json_ob.score
	def is_ticked(self, answer):
		return answer.json_ob.is_accepted
	def extract_text_from_node(self, node):
		str = ''
		for child in node.childNodes:
			if(child.firstChild == None):
				str = str + child.data
			else:
				str1 = self.extract_text_from_node(child)
				str = str + str1
		return str
	def get_xml_for_answer_body(self, answer):
		return '<jarvis>' + answer.body + '</jarvis>'
class DrakStackOverflowStackApp(DrakAbstractStackApp):
	def __init__(self):
		self.site = stackexchange.Site(stackexchange.StackOverflow, 'Y51JtGr4K7hqreoDcBURrQ((')
		self.site.be_inclusive()
class DrakAskUbuntuStackApp(DrakAbstractStackApp):
	def __init__(self):
		self.site = stackexchange.Site(stackexchange.AskUbuntu, 'Y51JtGr4K7hqreoDcBURrQ((')
		self.site.be_inclusive()

class DrakSuggestionFetcher():
	def __init__(self):
		self.so = DrakStackOverflowStackApp()
		self.au = DrakAskUbuntuStackApp()
	def get_suggestions(self, keywords, keyword_confidence):
		stackoverflow_query = keywords + " error stackoverflow"
		askubuntu_query = keywords + " error askubuntu"
		suggestions = []
		question_ids = []
		for url in search(stackoverflow_query, tld='es', lang='en', stop=5):
			hostname = urlparse.urlparse(url).hostname
			if(hostname == "stackoverflow.com"):
				path = urlparse.urlsplit(url).path
				pathx = str(path).split('/')
				question_ids.append(pathx[2])
		if len(question_ids)!=0:
			print utils.get_color("white") + "#DRAK : Fetched Stackoverflow Questions\n#DRAK : Fetching answers" + utils.reset_color()
			suggestions.extend(self.so.get_suggestions(question_ids))
			print utils.get_color("white") + "#DRAK : Answers fetched successfully" + utils.reset_color()
		question_ids = []
		for url in search(askubuntu_query, tld='es', lang='en', stop=5):
			hostname = urlparse.urlparse(url).hostname
			if(hostname == "askubuntu.com"):
				path = urlparse.urlsplit(url).path
				pathx = str(path).split('/')
				question_ids.append(pathx[2])
		if len(question_ids)!=0:
			print utils.get_color("white") + "#DRAK : Fetched AskUbuntu Questions\n#DRAK : Fetching answers" + utils.reset_color()
			suggestions.extend(self.au.get_suggestions(question_ids))
			print utils.get_color("white") + "#DRAK : Answers fetched successfully" + utils.reset_color()
		
		for suggestion in suggestions:
			suggestion.keyword_confidence = keyword_confidence
		return suggestions
'''
if __name__ == "__main__":
	app = DrakSuggestionFetcher()
	for suggestion in app.get_suggestions(raw_input("Enter key to be searched: "), 10):
		for code in suggestion.codes:
			print code
		print suggestion.confidence
		print "============================================="
'''
