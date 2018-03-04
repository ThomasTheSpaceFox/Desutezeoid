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

class plugobj:
	def __init__(self, plugname, plugclass, plugpath):
		self.plugname=plugname
		self.plugclass=plugclass
		self.plugpath=plugpath

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

