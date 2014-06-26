import os
import time
import sys
import subprocess

class DependencyChecker:
	def __init__(self,libname):
		self.libname = libname
		self.get_info()
	
	def get_info(self):
		try:
			dpkg_output = subprocess.check_output(['dpkg', '-s', self.libname])
			self.is_installed = "Package: "+self.libname+"\nStatus: install ok installed" in dpkg_output
		except:
			self.is_installed = False
	
class DependencySet:
	def __init__(self,dependency_list):
		self.dependency_list = []
		for dependency in dependency_list:
			self.dependency_list.append(DependencyChecker(dependency))
	
	def get_unmet_list(self):
		return [dependency.libname for dependency in self.dependency_list if not dependency.is_installed]
	
	def install_unmet(self):
		unmet = self.get_unmet_list()
		print "running","sudo apt-get install "+" ".join(unmet)
		os.system("sudo apt-get install "+" ".join(unmet))

def sanitise(content,data):	
	import time
	content=content.replace("{date}",time.strftime("%c"))
	for key in data:
		content = content.replace("{"+key+"}" , data[key])
	return content

def run_script(filename , highlight=False , sin=sys.stdin , sout=sys.stdout , verbose=True):
	start = time.time()
	
	fptr = open(filename)
	scripts = fptr.read().splitlines()
	fptr.close()
	
	for script in scripts:
		if verbose:
			print get_color("cyan" , -1 , "f") + script + reset_color()
		if highlight :
			print get_color("black" , "white" , "b"),
		sys.stdout.flush()
		sys.stderr.flush()
		
		try:
			subprocess.call(["bash" , "-c" , script] , stdin=sin , stdout=sout)
		except:
			raise Exception()
		
		if highlight:
				print reset_color(),
		sys.stdout.flush()
		sys.stderr.flush()
	end = time.time()
	
	print "\nTime Elapsed : " + str(end-start) + " sec"
def reset_color():
	return get_color(-1,-1,"reset")

def get_color(forecolor=-1 , backcolor=-1 , attr="default"):
	color={}
	color["black"]	= 0
	color["red"]	= 1
	color["green"]	= 2
	color["yellow"]	= 3
	color["blue"]	= 4
	color["magenta"]= 5
	color["cyan"]	= 6
	color["white"]	= 7
	
	mode={}
	mode["default"] = ""
	mode["reset"]	= "0;"
	mode["b"]	= "1;"
	mode["f"]	= "2;"
	mode["u"]	= "4;"
	mode["blink"] = "5;"
	
	string = ""
	try:
		fore = str(90 + color[forecolor]) + ";" if forecolor != -1 else ""
		back = str(100 + color[backcolor]) + ";" if backcolor != -1 else ""
		string =  fore + back + mode[attr]
	except:
		print get_color("red") + "Wrong code used " + reset_color()
		return ""
	
	#print string
	return "\033[" +  string + "52m"
