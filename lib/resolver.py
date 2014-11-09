import re
import sys
from ClosestWords import *
import subprocess


#dependency it requires aptitude search to be installed
def aptitude_search(module):
	output = subprocess.check_output(["aptitude","search",module])
	suggested_import = []
	for item in output.split("\n"):
		x = item.split()
		if len(x) != 0 :
			if x[0] == 'p':
				suggested_import.append(x[1])
	return suggested_import

class DrakeImmediateResolver:
	#path to look for similar files
	def __init__(self,log,path):
		self.log = log
		self.path = path
		self.import_regex = re.compile(r'(ImportError: No module named (\b\D*\b)).*')
		#file_not_found_regex = re.compile(r'(\b[^ ]*.h): No such file or directory')
		self.file_not_found_regex = re.compile(r'((\b[^ ]*): No such file or directory).*')
		self.command_regex = re.compile(r'((\b[^ ]*): command not found).*')
		self.error_regex = re.compile(r'(\w*Error):(.*:)*([^;:/]*).*')
		self.exception_regex = re.compile(r'(([^ .]*Exception): (([^;:.])*)) .*')

	def get_suggestion(self):
		solution = {}
		solution["suggestion"] = []
		solution["keyword"] = []

		for x in self.log:
			if self.import_regex.search(x)!=None:
				search = self.import_regex.search(x)
				target_module = search.group(2)
				suggested_modules = aptitude_search(target_module)
				suggestion = 'Did you mean to import one of the packages\n'+',  '.join(suggested_modules)+'\nYou need to install them first'
				if suggestion not in solution["suggestion"]:
					solution["suggestion"].append(suggestion)
					solution["keyword"].append(search.group(1))
					
			if self.file_not_found_regex.search(x)!=None:
				file_finder = ClosestWords(self.path)
				search = self.file_not_found_regex.search(x)
				target_word = search.group(2)
				suggested_file = file_finder.get_closest(target_word)
				suggestion = "Did u mean to include "+suggested_file
				if suggestion not in solution["suggestion"]:
					solution["suggestion"].append(suggestion)
					solution["keyword"].append(search.group(1))

			if self.command_regex.search(x)!=None:
				seach = self.command_regex.search(x)
				target_command = search.group(2)
			 	suggested_command = aptitude_search(target_command)
			 	suggestion = "Did u mean to use any of the following command\n"+",  ".join(suggested_command)+"\nYou need to install them first"
			 	if suggestion not in solution["suggestion"]:
					solution["suggestion"].append(suggestion)
					solution["keyword"].append(search.group(1))

		return solution
		
	def get_keywords(self):
		keywords = []
		for x in self.log:
			if self.error_regex.search(x)!=None:
				search = self.error_regex.search(x)
				keyword = search.group(1)+" "+search.group(3)
				if keyword not in keywords:
					keywords.append(keyword)
			if self.exception_regex.search(x)!=None:
				search = self.exception_regex.search(x)
				keyword = search.group(1)
				if keyword not in keywords:
					keywords.append(search.group(1))	
		return keywords		
'''	
def extract_text(path):
	logs = open("./logs/" + path,"rb").readlines()
	resolver = DrakeImmediateResolver(logs,["." , "jarvis" , "scripts" , "test"])
	
	result = {}
	result["immediate"] = resolver.get_suggestion()#["suggestion"]
	result["web"]  = resolver.get_keywords()
	return result
'''
