#!/usr/bin/python
import os
import readline
import utils
import signal
import sys
import traceback
import multiprocessing
import time

class JarvisInterpreter:
	
	def __init__(self):
		os.system("clear")
		self.trigger_list = []
		self.triggers	  = {}
		self.prompt		  = "Jarvis ~/ $ "
		self.status 	  = False
		self.stdinFD	  = sys.stdin.fileno()
		self.trigger_helplist = []
		self.is_child_trigger = {}
		self.is_operation     = {}
		self.init_triggers()
	
	def __del__(self):
		signal.signal(signal.SIGINT , signal.SIG_DFL)
	
	def start(self):
		signal.signal(signal.SIGINT , self.handler)
		self.status = True
		while(self.status == True):
			self.run()
	
	def handler(self , signum , frame):
		print utils.get_color("red") + "Keyboard interrrupt. Signal Number : " + str(signum) + utils.reset_color()
		print utils.get_color("white" , -1 , "b") + self.prompt + utils.reset_color() ,
		sys.stdout.flush()
		
	def child_handler(self , signum , frame):
		print utils.get_color("red") + "Keyboard interrrupt. Signal Number : " + str(signum) + utils.reset_color()
		print utils.get_color("white" , -1 , "b") + self.prompt + utils.reset_color() ,
		print utils.get_color("red") + "Exiting worker thread" + utils.reset_color()
		sys.stdout.flush()
		sys.stdin = os.fdopen(self.stdinFD)
		os._exit(0)
	
	def add_files(self):
		files = os.listdir(os.getcwd())
		def get_cmd(f):
			return lambda x : os.system("cat " + f)
		for f in files:
			if not os.path.isdir(f):
				self.add_trigger(f , get_cmd(f) , is_operation=False)
	
	def init_triggers(self):
		def exit_jarvis(arg):
			print utils.get_color("blue") + "Exiting Jarvis. Have a good day!!!" + utils.reset_color()
			self.__del__()
			self.status = False
		self.add_trigger("exit" , exit_jarvis,is_child=False , help_text="Exit jarvis")
		
		def chdir(arg):
			os.chdir(arg[0] if len(arg)>0 else os.getenv("HOME"))
		self.add_trigger("cd" , chdir,is_child=False , help_text="Change directory")
		
		self.add_trigger("help",self.print_help , help_text="Help command for command line interface")
	
	def add_trigger(self , name , proc , is_child=True , help_text="" , is_operation=True):
		if not self.triggers.has_key(name):
			self.triggers[name] = proc
			self.trigger_list.append(name)
			self.trigger_helplist.append(help_text)
			self.is_child_trigger[name] = is_child
			self.is_operation[name] = is_operation
	
	def print_help(self,arg):
		for i in range(len(self.trigger_list)):
			if self.is_operation[self.trigger_list[i]]:
				print utils.get_color("cyan") + self.trigger_list[i] + utils.reset_color()
				print utils.get_color("yellow",attr="b") + self.trigger_helplist[i] + utils.reset_color() + "\n"
	
	def complete_type(self,text, state):
		for cmd in self.trigger_list:
			if cmd.startswith(text):
				if not state:
					return cmd
				else:
					state -= 1
	
	def start_trigger(self,fd,trigger,arg):
		try:
			self.stdinFD = sys.stdin.fileno()
			sys.stdin    = os.fdopen(fd)
			signal.signal(signal.SIGINT , self.child_handler)
			trigger(arg)
		except OSError:
			print utils.get_color("red") + "Trigger interrupted" + utils.reset_color()
	
	def run(self):
		self.add_files()
		readline.parse_and_bind("tab: complete")
		readline.set_completer(self.complete_type)
		cmd = str(raw_input(utils.get_color("white" , -1 , "b") + self.prompt + utils.reset_color()))
		cmd = cmd.split()
		if len(cmd)==0 :
			return
		try:
			if cmd[0] in self.trigger_list:
				if self.is_child_trigger[cmd[0]]:
					proc = multiprocessing.Process(name='worker:'+cmd[0], target=self.start_trigger,args=(self.stdinFD,self.triggers[cmd[0]],cmd[1:len(cmd)],))
					proc.start()
					proc.join()
				else:
					self.triggers[cmd[0]](cmd[1:len(cmd)])
			else:
				os.system(" ".join(cmd))
		except SystemExit :
			sys.exit(0)
		except Exception:
			print utils.get_color("red") + "Error executing trigger" + utils.reset_color()
			traceback.print_exc(file=sys.stdout)
			
