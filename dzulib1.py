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
pygame.display.init()
#this library should contain any functions and data needed by dezutezeoid
#that don't need to be in the actual engine executable

#some functions do rely on variables only present within DZU-ENG1.py however.
print ("dzulib initalized")
#inital main.sav file structure
savtree='''<?xml version="1.0" encoding="UTF-8"?>
<sav>
	<keysav>
	</keysav>
</sav>
'''
#main.sav init.
def initmainsave():
	print ('Initalize main.sav')
	mainsavfile = open('main.sav', 'w')
	mainsavfile.write(savtree)
	mainsavfile.close()

#image scrollers
def vscroll(scrollval, image):
	offs=image.get_height()
	newimage=image.copy()
	newimage.fill((0, 0, 0, 0))
	newimage.blit(image, (0, scrollval))
	if (str(scrollval))[0]=="-":
		newimage.blit(image, (0, (scrollval + offs)))
	else:
		newimage.blit(image, (0, (scrollval - offs)))
	return newimage

def hscroll(scrollval, image):
	offs=image.get_width()
	newimage=image.copy()
	newimage.fill((0, 0, 0, 0))
	newimage.blit(image, (scrollval, 0))
	if (str(scrollval))[0]=="-":
		newimage.blit(image, ((scrollval + offs), 0))
	else:
		newimage.blit(image, ((scrollval - offs), 0))
	return newimage

imagepath='img'

filedict={}
textdict={}
def filelookup(filename):
	global filedict
	if filename in filedict:
		return filedict[filename]
	else:
		if (filename.lower()).endswith(".jpg") or (filename.lower()).endswith(".jpeg") or (filename.lower()).startswith("no-tr"):
			imgret=pygame.image.load(os.path.join(imagepath, filename)).convert()
		else:
			imgret=pygame.image.load(os.path.join(imagepath, filename)).convert_alpha()
		filedict[filename]=imgret
		return imgret

def textrender(text, size, fgcolor, bgcolor, transp):
	global textdict
	keyx=(text + str(size) + fgcolor + bgcolor + str(transp))
	if keyx in textdict:
		return textdict[keyx]
	else:
		fgcolor=pygame.Color(fgcolor)
		bgcolor=pygame.Color(bgcolor)
		texfnt=pygame.font.SysFont(None, size)
		if transp==0:
			texgfx=texfnt.render(text, True, fgcolor, bgcolor)
		else:
			texgfx=texfnt.render(text, True, fgcolor)
		textdict[keyx]=texgfx
		return texgfx

class clicktab:
	def __init__(self, box, reftype, ref, keyid, takekey, sfxclick, sound, quitab=0):
		self.box=box
		self.ref=ref
		self.keyid=keyid
		self.takekey=takekey
		self.reftype=reftype
		self.sfxclick=sfxclick
		self.sound=sound
		self.quitab=quitab