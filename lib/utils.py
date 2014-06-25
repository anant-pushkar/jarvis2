import os
import time
import sys
import subprocess

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
