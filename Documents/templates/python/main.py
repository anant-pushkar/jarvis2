'''
Project name : {name}
Created on : {date}
Author : {author}
{comments}
'''
import sys
debug_mode = len(sys.argv)>1 and sys.argv[1]=="DEBUG"
def debug(msg):
	if debug_mode:
		print msg