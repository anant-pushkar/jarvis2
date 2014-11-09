import re
import sys
from os import listdir
import os.path
from collections import defaultdict
debug_mode = len(sys.argv)>1 and sys.argv[1]=="DEBUG"
def debug(msg):
	if debug_mode:
		print msg

class ClosestWords:
	def __init__(self,path):
		self.corpus = []
		#expecting list of the paths
		for dir_name in path:
			for file in os.listdir(dir_name):
				self.corpus.append(file)
			
		self.cost = {}
		self.cost["delete"] = 1
		self.cost["insert"] = 2
		self.cost["replace"]= 1
		self.cost["swap"]	= 1
	
	def get_edit_dist(self , start , target):
		#print start,target
		x = len(start)+1
		y = len(target)+1
		lookup = [[ 0 for i in xrange(y)] for j in xrange(x)]
		
		for i in xrange(1,x):
			lookup[i][0] = self.cost["delete"] + lookup[i-1][0]
		
		for i in xrange(1,y):
			lookup[0][i] = self.cost["insert"] + lookup[0][i-1]
		
		for i in xrange(1,x):
			check = False
			for j in xrange(1,y):
				cost_list = range(len(self.cost.keys()))
				cost_list[0] = lookup[i-1][j] + self.cost["delete"]
				cost_list[1] = lookup[i][j-1] + self.cost["insert"]
				cost_list[2] = lookup[i-1][j-1] + (self.cost["replace"] if start[i-1]!=target[j-1] else 0)
				cost_list[3] = (lookup[i-2][j-2] + self.cost["swap"]) if i>1 and j>1 and start[i-1]==target[j-2] and start[i-2]==target[j-1] else (max([x,y])+2)
				
				lookup[i][j] = min(cost_list)
				check = check or lookup[i][j]<self.closest_val
			if not check:
				return sys.maxint
		'''
		for i in xrange(x):
			print lookup[i]
		'''
		return lookup[x-1][y-1]
	
	def get_closest(self , txt):
		self.closest_val = sys.maxint
		closest_word= []
		extension = os.path.splitext(txt)[1]
		for word in self.corpus:
			dist = self.get_edit_dist(word , txt)#*self.lim + self.corpus[word]
			if self.closest_val>dist:
				self.closest_val = dist
				closest_word = [word]
			elif self.closest_val==dist:
				closest_word.append(word)
		
		closest_word.sort()
		return closest_word[0];
















