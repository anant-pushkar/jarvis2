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
		mimetypes.add_type('text/php_source_code','.php')
		mimetypes.add_type('text/yaml_file','.yaml')
	
	def is_text(self,filename):
		tp = mimetypes.guess_type(filename)
		print filename , tp
		try:
			return "text/" in tp[0]
		except:
			return False
	
	def add_admin_triggers(self):
		def create_project(arg):
			import readline
			types = os.listdir(os.getenv("HOME")+"/Documents/jarvis/templates")
			print utils.get_color("cyan") + "Select a project type : " 
			for tp in types:
				print "\t" , tp 
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
			files = os.listdir(type_folder)
			
			def span_dir(name):
				os.system("mkdir " + os.path.join(project_folder , name))
				for folder in os.listdir(os.path.join(type_folder , name)):
					if not folder.startswith("."):
						if os.path.isdir(os.path.join(os.path.join(type_folder , name), folder)):
							span_dir(os.path.join(name,folder))
						elif os.path.isfile(os.path.join(os.path.join(type_folder , name), folder)):
							files.append(os.path.join(name,folder))
			
			for fname in files:
				if os.path.isdir(os.path.join(type_folder,fname)):
					span_dir(fname)
			
			mainfiles = []
			for fname in files:
				path = os.path.join(project_folder,fname)
				if os.path.isfile(os.path.join(type_folder,fname)):
					if path.count("/")==project_folder.count("/")+1 : 
						mainfiles.append(path)
					fptr = open(os.path.join(type_folder,fname))
					content = fptr.read()
					fptr.close()
					print utils.get_color("blue") + "Creating " + fname + utils.reset_color()
					fptr = open(path , "w")
					fptr.write(utils.sanitise(content,{"name":name , "comments":cmt , "author":str(j["author"]) , "workspace":str(j["workspace"])}))
					fptr.close()
			
			os.chdir(project_folder)
			os.system("gnome-terminal -e jarvis &")
			cmd=str(j["editor"])+" " + " ".join([filename for filename in mainfiles if self.is_text(filename)])+" &"
			os.system(cmd)
		
		self.add_trigger("create_project" , create_project , help_text="Create a new project")
		
		def open_project(arg):
			import readline
			types = os.listdir(os.getenv("HOME")+"/Documents/jarvis/templates")
			print utils.get_color("cyan") + "Select a project type : " 
			for tp in types:
				print "\t" , tp 
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
				path = os.path.join(project_folder,fname)
				if os.path.isfile(os.path.join(project_folder,fname)):
					mainfiles.append(path)
			os.chdir(project_folder)
			os.system("gnome-terminal -e jarvis &")
			cmd=str(j["editor"])+" " + " ".join([filename for filename in mainfiles if self.is_text(filename)])+" &"
			os.system(cmd)
		
		self.add_trigger("open_project",open_project,help_text="Open Existing project")
		
		def update(arg):
			os.system("mkdir -p .jarvis_update_repo")
			os.chdir(".jarvis_update_repo")
			
			print utils.get_color("blue") + "Cloning Repository in current directory" + utils.reset_color()
			os.system("git clone https://github.com/anant-pushkar/jarvis2.git")
			
			print utils.get_color("blue") + "Installing updates" + utils.reset_color()
			os.chdir("jarvis2")
			os.system("bash update.sh")
			
			print utils.get_color("blue") + "Cleaning Repository" + utils.reset_color()
			os.chdir("../..")
			os.system("rm -r .jarvis_update_repo")
			
		self.add_trigger("update",update,help_text="Update Jarvis")import project
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
		mimetypes.add_type('text/php_source_code','.php')
		mimetypes.add_type('text/yaml_file','.yaml')
	
	def is_text(self,filename):
		tp = mimetypes.guess_type(filename)
		print filename , tp
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
			files = files + ["scripts/"+fname for fname in os.listdir(type_folder + "/scripts")]
			mainfiles = []
			for fname in files:
				path = project_folder + "/" + fname
				if(os.path.isfile(type_folder + "/" + fname)):
					mainfiles.append(path)
					fptr = open(type_folder + "/" + fname)
					content = fptr.read()
					fptr.close()
					print utils.get_color("blue") + "Creating " + fname + utils.reset_color()
					fptr = open(path , "w")
					fptr.write(utils.sanitise(content,{"name":name , "comments":cmt , "author":str(j["author"]) , "workspace":str(j["workspace"])}))
					fptr.close()
			
			os.chdir(project_folder)
			os.system("gnome-terminal -e jarvis &")
			cmd=str(j["editor"])+" " + " ".join([filename for filename in mainfiles if self.is_text(filename)])+" &"
			os.system(cmd)
		
		self.add_trigger("create_project" , create_project , help_text="Create a new project")
		
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
		
		self.add_trigger("open_project",open_project,help_text="Open Existing project")
		
		def update(arg):
			os.system("mkdir -p .jarvis_update_repo")
			os.chdir(".jarvis_update_repo")
			
			print utils.get_color("blue") + "Cloning Repository in current directory" + utils.reset_color()
			os.system("git clone https://github.com/anant-pushkar/jarvis2.git")
			
			print utils.get_color("blue") + "Installing updates" + utils.reset_color()
			os.chdir("jarvis2")
			os.system("bash update.sh")
			
			print utils.get_color("blue") + "Cleaning Repository" + utils.reset_color()
			os.chdir("../..")
			os.system("rm -r .jarvis_update_repo")
			
		self.add_trigger("update",update,help_text="Update Jarvis")
