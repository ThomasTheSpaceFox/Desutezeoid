#!/usr/bin/env python
import pygame.event
import pygame.key
import pygame.display
import pygame.image
import pygame.mixer
import pygame
import sys
import time
import os
import dzulib1 as dzulib
pygame.display.init()
import traceback
import random
import xml.etree.ElementTree as ET
pluglist=[]


class BUILTIN_imgscroll:
	def __init__(self, screensurf, keylist, vartree):
		self.screensurf=screensurf
		self.keylist=keylist
	def fork(self, tagobj):
		return
	def core(self, tagobj):
		return
	def pump(self):
		return
	def click(self, event):
		return
	def clickup(self, event):
		return
	def pageclear(self):
		return
	def imageloader(self, filename):
		filenlist=filename.split("--")
		#print(filename)
		if filenlist[0]=="imageoffset":
			hscroll=int(filenlist[1].replace("n", "-"))
			vscroll=int(filenlist[2].replace("n", "-"))
			imagex=dzulib.filelookup("--".join(filenlist[3:]))
			return dzulib.vscroll(vscroll, dzulib.hscroll(hscroll, imagex))


class plugobj:
	def __init__(self, plugname, plugclass, plugpath):
		self.plugname=plugname
		self.plugclass=plugclass
		self.plugpath=plugpath
builtins=[plugobj("image_wrapped_offset_synthax", BUILTIN_imgscroll, "BUILT-IN")]
Plugpath="plugins"
for plugcodefile in os.listdir(Plugpath):
	if plugcodefile.lower().endswith(".dzup.py"):
		PLUGFILE=open(os.path.join(Plugpath, plugcodefile), 'r')
		try:
			PLUGEXEC=compile(PLUGFILE.read(), os.path.join(Plugpath, plugcodefile), 'exec')
			exec(PLUGEXEC)
			pluginst=plugobj(plugname, plugclass, plugpath)
			pluglist.extend([pluginst])
			print(("Load plugin: " + plugname + " (" + plugcodefile + ")"))
		except SyntaxError as err:
			print(("Plugin failure: SyntaxError on " + plugcodefile))
			print((traceback.format_exc()))

for plugcode in builtins:
	print(("Load BUILTIN: " + plugcode.plugname))
	pluglist.extend([plugcode])
	