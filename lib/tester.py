#!/usr/bin/python
import utils
import json
import subprocess
import project
import os
import sys
import importlib

class JarvisFilter:
	
	def __init__(self , filename):
		fptr = open(filename)
		jObject = json.load(fptr)
		fptr.close()
		
		self.name  = str(jObject["name"])
		self.build_script = str(jObject["build"])
		self.run_script   = str(jObject["run"])
	
	def build(self):
		os.system(self.build_script)
		
	def run(self):
		os.system(self.run_script)
class JarvisTestError:
	
	def __init__( self , msg ):
		self.msg = msg
class JarvisTester:
	
	def __init__(self , prj):
		self.project = prj
		
		fptr = open("test/filters.json")
		jObject = json.load(fptr)
		fptr.close()
		
		self.filter_list = []
		for fltr in jObject["list"]:
			self.filter_list.append(JarvisFilter("test/" + str(fltr) + "/config.json"))
	
	def build_filters(self):
		print utils.get_color("blue") + "Building Filters..." + utils.reset_color()
		for fltr in self.filter_list:
			fltr.build()
			print utils.get_color("green") + fltr.name + " built successfully"
		print utils.reset_color()
	
	def create_input(self):
		for i in range(len(self.tests)):
			print utils.get_color("blue") + "Creating files for " + self.tests[i].description + utils.reset_color()
			inputStr = ""
			if self.tests[i].header!="":
				inputStr = inputStr + self.tests[i].header + "\n"
			if self.tests[i].print_count : inputStr= inputStr + str(len(self.tests[i].instances)) + "\n"
			for j in range( len( self.tests[i].instances ) ):
				inputStr = inputStr + self.tests[i].instances[j].getInput() + "\n"
			if self.tests[i].footer!="":
				inputStr = inputStr + self.tests[i].footer + "\n"
			f = open( self.tests[i].description.replace(" ","_") , "w+" )
			f.write(inputStr)
			f.close()
			print utils.get_color("green") + "Files created" + utils.reset_color() + "\n"
	
	def build(self):
		self.build_filters()
		self.create_input()
		
		print utils.get_color("blue") + "Creating test scripts" + utils.reset_color()
		
		string = "("
		fptr = open("scripts/" + self.project.runfile)
		scripts = fptr.read().splitlines()
		fptr.close()
		
		for script in scripts:
			string = string + script + ";"
		string = string + ")"
		
		for fltr in self.filter_list:
			string = string + " | " + fltr.run_script
		
		fptr = open("scripts/testfile" , "w")
		fptr.write(string)
		fptr.close()
		
		print utils.get_color("green") + "Test scripts created" + utils.reset_color() + "\n"
	
	def throw_eof(self , i , line,instance):
		print utils.get_color("red") ,
		print instance.description + " cannot read after line #" +str(i) + " :\n\t" + line
		print utils.reset_color()
		raise JarvisTestError("Unexpected End Of Input")
	
	def run_instance(self , o_str , instance, index):
		e_list = instance.outputStr.split("\n")
		if(e_list[0] == "?"):
			print "Showing output for " + instance.description
			print utils.get_color("yellow")
			if len(e_list)>2 and e_list[2] != "false" : 
				print "input : " 
				print instance.inputStr
			print "output : "
			for i in range(int(e_list[1])):
				if index >= len(o_str):
					self.throw_eof(i , e_list[i],instance)
				print o_str[index]
				index = index + 1
			print utils.reset_color()
			return index
		for i in range(len(e_list)):
			exp = e_list[i]
			if exp=="":
				continue
			if index >= len(o_str) :
				self.throw_eof(i , e_list[i],instance)
			if not instance.test(o_str[index] , exp):
				print utils.get_color("red") 
				print instance.description + " failed at line#" + str(i)
				print "Expected : " + exp
				print "Got      : " + o_str[index]
				print utils.reset_color()
				raise JarvisTestError("Mismatch")
			index = index + 1
		return index
	
	def examine(self , o_str , test):
		print utils.get_color("blue") + "Examining Output" + utils.reset_color()
		o_list = o_str.split("\n")
		index  = 0
		try:
			for instance in test.instances:
				index = self.run_instance(o_list , instance , index)
			print utils.get_color("green") + test.description + " passed" + utils.reset_color()
		except JarvisTestError as err:
			print utils.get_color("red") + test.description + " falied due to : " ,
			print err.msg + utils.reset_color()

	def test(self):
		if "testCases" in sys.modules.keys():
			del sys.modules["testCases"]
		self.tests = importlib.import_module("testCases").getTests()
		self.build()
		for i in range(len(self.tests)):
			print utils.get_color("blue") + "Running " + self.tests[i].description + utils.reset_color()
			self.examine(subprocess.check_output(["bash" , "scripts/testfile"] , stdin=open(self.tests[i].description.replace(" ","_"))) , self.tests[i])
			print ""
