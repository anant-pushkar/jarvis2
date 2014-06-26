import project
import jarvis_interpreter as jarvis
import sys
import importlib
import os
import utils
import json
import mimetypes

class JarvisAdminInterpreter(jarvis.JarvisInterpreter):
	def __init__(self):
		jarvis.JarvisInterpreter.__init__(self)
		self.add_admin_triggers()
	
	def is_text(self,filename):
		tp = mimetypes.guess_type(filename)
		print tp
		try:
			return "text/" in tp[0]
		except:
			return False
	
	def add_admin_triggers(self):
		def create_project(arg):
			import readline
			types = os.listdir(os.getenv("HOME")+"/Documents/jarvis/templates")
			print utils.get_color("cyan") + "Select a project type : " 
			print "\t" ,
			for tp in types:
				print tp + " " ,
			print utils.reset_color()
			
			readline.parse_and_bind("tab: complete")
			def complete_type(text, state):
				for tp in types:
					if tp.startswith(text):
						if not state:
							return tp
						else:
							state -= 1	
			readline.set_completer(complete_type)
			tp = str(raw_input(utils.get_color("blue") + "Enter Type : " + utils.reset_color()))
			check = tp in types 
			while not check:
				readline.parse_and_bind("tab: complete")
				readline.set_completer(complete_type)
				tp  =str(raw_input(utils.get_color("blue") + "Project Type not recognized. \nEnter type     : " + utils.reset_color()))
				check = tp in types 
				
			name = str(raw_input(utils.get_color("blue") + "Enter Name : " + utils.reset_color()))
			name = name.replace("(","_")
			name = name.replace(")","_")
			cmt  = str(raw_input(utils.get_color("blue") + "Enter Comments : " + utils.reset_color()))
			name = name.replace(" ","_")
			
			f=open(os.getenv("HOME")+"/Documents/jarvis/config.json")
			j=json.load(f)
			f.close()
			
			project_folder = os.getenv("HOME") + "/" + str(j["workspace"]) + "/" + tp + "/" + name
			if os.path.exists(project_folder):
				print utils.get_color("red") + "Project already exists" + utils.reset_color()
				return
			type_folder = os.getenv("HOME")+"/Documents/jarvis/templates/" + tp
			os.system("mkdir " + project_folder)
			
			os.system("cp -R " + type_folder + "/jarvis "  + project_folder )
			os.system("cp -R " + type_folder + "/scripts "  + project_folder)
			os.system("cp -R " + type_folder + "/test "  + project_folder   )
			
			files = os.listdir(type_folder)
			mainfiles = []
			for fname in files:
				if fname.startswith("main") or fname=="project.json":
					mainfiles.append(project_folder + "/" + fname)
					fptr = open(type_folder + "/" + fname)
					content = fptr.read()
					fptr.close()
					print utils.get_color("blue") + "Creating " + fname + utils.reset_color()
					fptr = open(project_folder + "/" + fname , "w")
					fptr.write(utils.sanitise(content,{"name":name , "comments":cmt , "author":str(j["author"])}))
					fptr.close()
			
			os.chdir(project_folder)
			os.system("gnome-terminal -e jarvis &")
			cmd=str(j["editor"])+" " + " ".join([filename for filename in mainfiles if self.is_text(filename)])+" &"
			os.system(cmd)
		
		self.add_trigger("create_project" , create_project)
		
		def open_project(arg):
			import readline
			types = os.listdir(os.getenv("HOME")+"/Documents/jarvis/templates")
			print utils.get_color("cyan") + "Select a project type : " 
			print "\t" ,
			for tp in types:
				print tp + " " ,
			print utils.reset_color()
			
			readline.parse_and_bind("tab: complete")
			def complete_type(text, state):
				for tp in types:
					if tp.startswith(text):
						if not state:
							return tp
						else:
							state -= 1	
			readline.set_completer(complete_type)
			tp = str(raw_input(utils.get_color("blue") + "Enter Type : " + utils.reset_color()))
			check = tp in types 
			while not check:
				readline.parse_and_bind("tab: complete")
				readline.set_completer(complete_type)
				tp  =str(raw_input(utils.get_color("blue") + "Project Type not recognized. \nEnter type     : " + utils.reset_color()))
				check = tp in types 
			
			f=open(os.getenv("HOME")+"/Documents/jarvis/config.json")
			j=json.load(f)
			f.close()
			project_folder = os.getenv("HOME") + "/" + str(j["workspace"]) + "/" + tp 
			project_list   = os.listdir(project_folder)
			project_list.sort()
			
			print utils.get_color("cyan") + "Select project : " + utils.reset_color()
			for prj in project_list:
				print utils.get_color("yellow",attr="b") + prj + utils.reset_color()
				try:
					jObj = json.load(open(project_folder+"/"+prj+"/project.json"))
					if "description" in jObj.keys():
						print utils.get_color("blue") + "\t" + jObj["description"] + utils.reset_color() + "\n"
				except:
					print utils.get_color("red") + "\tError while reading config files. Please check "+prj+"/project.json\n" + utils.reset_color()
				
			print utils.reset_color();
			readline.parse_and_bind("tab: complete")
			def complete_name(text, state):
				for prj in project_list:
					if prj.startswith(text):
						if not state:
							return prj
						else:
							state -= 1	
			readline.set_completer(complete_name)
			name = str(raw_input(utils.get_color("blue") + "Enter Name : " + utils.reset_color()))
			check = name in project_list
			while not check:
				readline.parse_and_bind("tab: complete")
				readline.set_completer(complete_name)
				name  =str(raw_input(utils.get_color("blue") + "Project Name not recognized. \nEnter name     : " + utils.reset_color()))
				check = name in project_list
			
			project_folder = project_folder + "/" + name + "/"
			
			files = os.listdir(project_folder)
			mainfiles = []
			for fname in files:
				if (fname.startswith("main") and "." in fname) or fname=="project.json":
					mainfiles.append(fname)
			os.chdir(project_folder)
			os.system("gnome-terminal -e jarvis &")
			cmd=str(j["editor"])+" " + " ".join([filename for filename in mainfiles if self.is_text(filename)])+" &"
			os.system(cmd)
		
		self.add_trigger("open_project",open_project)
			
		

