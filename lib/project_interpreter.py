import project
import jarvis_interpreter as jarvis
import sys
import importlib
import os
import json
import subprocess
import utils
from  resolver import *
from DrakSuggestionsFetcher import *
from inex import *

class JarvisProjectInterpreter(jarvis.JarvisInterpreter):
	
	def __init__(self , prj):
		jarvis.JarvisInterpreter.__init__(self)
		self.project = prj
		self.add_project_triggers()
		self.prompt  = "Jarvis ~/" + prj.name + "$ "
	
	def __extract_text__(self , path):
		logs = open("./" + path,"rb").readlines()
		resolver = DrakeImmediateResolver(logs,["." , "jarvis" , "scripts" , "test"])
	
		result = {}
		result["immediate"] = resolver.get_suggestion()#["suggestion"]
		result["web"]  = resolver.get_keywords()
		return result
	
	def __run_drak__(self , filename):
		text_extract = self.__extract_text__(filename)
		if len(text_extract["immediate"]["suggestion"])!=0:
			print utils.get_color("blue") + "Immediately resolvable Issues detected" + utils.reset_color()
			for suggestion in text_extract["immediate"]["suggestion"]:
				print utils.get_color("yellow") + suggestion + utils.reset_color()
				
		response = str(raw_input(utils.get_color("blue") + "Would you like to search online for better suggestions?[Y/N]" + utils.reset_color())).lower()
		if response == "y":
			app = DrakSuggestionFetcher()

			web_result = []
			for keyword in text_extract["web"] + text_extract["immediate"]["keyword"]:
				web_result += app.get_suggestions(keyword, 10)
			ob = Inex()
			print utils.get_color("blue") + "Dr Drak Suggests : " + utils.reset_color()
			print utils.get_color("yellow") + ob.processInput(web_result , False) + utils.reset_color()
	def  add_project_triggers(self):
		self.add_files()
		
		def run_project(arg):
			sin = 0 if len(arg)<1 else arg[0]
			sout= 0 if len(arg)<2 else arg[1]
			self.project.run(sin , sout)
		self.add_trigger("run" , run_project , help_text="Run the current project")
		
		def debug_project(arg):
			sin = 0 if len(arg)<1 else arg[0]
			sout= 0 if len(arg)<2 else arg[1]
			self.project.debug(sin , sout)
		self.add_trigger("debug" , debug_project , help_text="Run project in debug mode")
		
		def build_project(arg):
			self.project.build()
		self.add_trigger("build" , build_project , is_child=False , help_text="Build Project")
		
		def test_project(arg):
			if "tester" in sys.modules.keys():
				del sys.modules["tester"]
			tester = importlib.import_module("tester")
			jarvistester = tester.JarvisTester(self.project)
			jarvistester.test()
		self.add_trigger("test" , test_project , help_text="Test Project")
		
		def drak_fixit(arg):
			if not os.path.isdir("./logs"):
				print utils.get_color("yellow") + "Creating log folder" + utils.reset_color()
				os.mkdir("./logs")
				
			self.project.build(err = open('logs/build_error', 'w'))
			if os.stat('logs/build_error').st_size > 1:
				print utils.get_color("red") + "Build Error Encountered" + utils.reset_color()
				print utils.get_color("blue") + "Analyzing for possible Build Errors" + utils.reset_color()
				self.__run_drak__('logs/build_error')
			
			self.project.run(err = open('logs/run_error', 'w'))
			if os.stat('logs/run_error').st_size > 1:
				print utils.get_color("red" , attr="b") + "Run Time Error Encountered" + utils.reset_color()
				print utils.get_color("blue") + "Analyzing for possible Run Errors" + utils.reset_color()
				self.__run_drak__('logs/run_error')
			
			os.remove('logs/build_error')
			os.remove('logs/run_error')
			
		self.add_trigger("drak_fixit" , drak_fixit , help_text="Use Drak to resolve dependency Issues")
			
		
		def install_dependency(arg):
			self.project.install_dependency()
		self.add_trigger("install_dependency",install_dependency , help_text="Install Dependencies")
		
		def add_module(arg):
			fptr = open(os.getcwd() + "/project.json")
			j = json.load(fptr)
			tp  = str(j["type"])
			name= str(j["name"])
			fptr.close()
			
			f=open(os.getenv("HOME")+"/Documents/jarvis/config.json")
			j=json.load(f)
			workspace =  str(j["workspace"])
			author    =  str(j["author"])
			f.close()
			
			project_folder = os.getenv("HOME") + "/" + workspace + "/" + tp + "/" + name
			type_folder = os.getenv("HOME")+"/Documents/jarvis/templates/" + tp
			
			module_name = str(raw_input(utils.get_color("blue") + "Enter Module Name : " + utils.reset_color()))
			module_name = module_name.replace(" ","_")
			
			files = os.listdir(type_folder)
			ls = os.listdir(os.getcwd())
			for fname in files:
				if fname.startswith("module"):
					fname = fname.replace("module",module_name)
					if fname in ls:
						print utils.get_color("red") + "Cannot add "+module_name+" : file " + fname + " already exists" + utils.reset_color()
						return 
			
			cmt = str(raw_input(utils.get_color("blue") + "Comments : " + utils.reset_color()))
			
			for fname in files:
				if fname.startswith("module"):
					fptr = open(type_folder + "/" + fname)
					content = fptr.read()
					fptr.close()
					fname = fname.replace("module",module_name)
					print utils.get_color("blue") + "Creating " + fname + utils.reset_color()
					fptr = open(project_folder + "/" + fname , "w")
					fptr.write(utils.sanitise(content,{"name":name , "comments":cmt , "author":author,"module":module_name}))
					fptr.close()
			print utils.get_color("green") + "Module Added" + utils.reset_color()
			
		self.add_trigger("add_module",add_module , help_text="Add new modules using pre-defined templates")

