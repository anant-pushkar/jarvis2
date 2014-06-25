import project
import jarvis_interpreter as jarvis
import sys
import importlib
import os
import json
import utils

class JarvisProjectInterpreter(jarvis.JarvisInterpreter):
	
	def __init__(self , prj):
		jarvis.JarvisInterpreter.__init__(self)
		self.project = prj
		self.add_project_triggers()
		self.prompt  = "Jarvis ~/" + prj.name + "$ "
		
	def  add_project_triggers(self):
		self.add_files()
		
		def run_project(arg):
			sin = 0 if len(arg)<1 else arg[0]
			sout= 0 if len(arg)<2 else arg[1]
			self.project.run(sin , sout)
		self.add_trigger("run" , run_project)
		
		def debug_project(arg):
			sin = 0 if len(arg)<1 else arg[0	]
			sout= 0 if len(arg)<2 else arg[1]
			self.project.debug(sin , sout)
		self.add_trigger("debug" , debug_project)
		
		def build_project(arg):
			self.project.build()
		self.add_trigger("build" , build_project)
		
		def test_project(arg):
			if "tester" in sys.modules.keys():
				del sys.modules["tester"]
			tester = importlib.import_module("tester")
			jarvistester = tester.JarvisTester(self.project)
			jarvistester.test()
		self.add_trigger("test" , test_project)
		
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
			
		self.add_trigger("add_module",add_module)

