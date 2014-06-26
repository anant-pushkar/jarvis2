#!/usr/bin/python
import json
import utils
import sys

class JarvisProject: 
	
	def __init__( self , filename ):
		fptr = open(filename)
		jObject = json.load(fptr)
		fptr.close()
		
		self.name 			= str(jObject["name"])
		self.description	= str(jObject["description"])
		self.buildfile		= str(jObject["buildfile"])
		self.runfile		= str(jObject["runfile"])
		self.debugfile		= str(jObject["debugfile"])
		self.set_verbose	= False
		self.dependency_set	= utils.DependencySet(jObject["dependency"] if "dependency" in jObject.keys() else [])
		self.warn_for_dependency()
	
	def warn_for_dependency(self):
		unmet = self.dependency_set.get_unmet_list()
		if len(unmet)!=0:
			print utils.get_color("red") + "The following dependencies seem to be unmet. You better make sure these are installed before building the project" + utils.reset_color()
			for dependency in unmet:
				print utils.get_color("yellow") + dependency + utils.reset_color()
			print utils.get_color("blue") + "Or you could simply use install_dependency command otherwise" + utils.reset_color()
			return False
		return True
	
	def install_dependency(self):
		unmet = self.dependency_set.get_unmet_list()
		if len(unmet)!=0:
			print utils.get_color("cyan") + "Installing : " + " ".join(unmet) + utils.reset_color()
			self.dependency_set.install_unmet()
		else:
			print utils.get_color("cyan") + "Nothing to install" + utils.reset_color()
	
	def printInfo(self):
		print "Project Name : " + self.name
		print "Description  : " + self.description
		print "Build File : " + self.buildfile
		print "Debug File : " + self.debugfile
		print "Run File   : " + self.runfile
	
	def build(self):
		self.warn_for_dependency()
		print utils.get_color("blue" , -1 , "b") + "Building Project...\n" + utils.reset_color()
		try:
			utils.run_script("scripts/" + self.buildfile , verbose = self.set_verbose)
		except Exception as err:
			print err
		print utils.get_color("blue" , -1 , "b") + "Build Complete" + utils.reset_color()
	
	def get_file(self , name , alter_stream , mode="r"):
		if(name!=0):
			try:
				sin=open(name , mode)
			except:
				print utils.get_color("red") + "Could not open " + name 
				print "Using " + alter_stream.name + " instead"
				sin = alter_stream
		else:
			sin=alter_stream
		return sin
	
	def run(self , iname=0 , oname=0):
		sin = self.get_file(iname , sys.stdin)
		sout= self.get_file(oname , sys.stdout , "w")
		print utils.get_color("blue" , -1 , "b") + "Running Project...\n" + utils.reset_color()
		try:
			utils.run_script("scripts/" + self.runfile , True , sin , sout , verbose = self.set_verbose)
		except Exception as err:
			print err.args
		print utils.get_color("blue" , -1 , "b") + "Run Complete" + utils.reset_color()
		
	def debug(self , iname=0 , oname=0):
		sin = self.get_file(iname , sys.stdin)
		sout= self.get_file(oname , sys.stdout , "w")
		print utils.get_color("blue" , -1 , "b") + "Debugging Project...\n" + utils.reset_color()
		try:
			utils.run_script("scripts/" + self.debugfile , True , sin , sout , verbose = self.set_verbose)
		except Exception as err:
			print err.args
		print utils.get_color("blue" , -1 , "b") + "Debug Complete\n" + utils.reset_color()
		
#prj = JarvisProject("project.json")
#prj.printInfo()
#prj.build()
#prj.debug()
#prj.run()