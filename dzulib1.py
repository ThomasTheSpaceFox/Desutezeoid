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
	<plugsav>
	</plugsav>
	<pagelink/>
</sav>
'''
#main.sav init.
def initmainsave():
	print ('Initalize main.sav')
	mainsavfile = open(os.path.join("save", 'autosave.sav'), 'w')
	mainsavfile.write(savtree)
	mainsavfile.close()

def definepluginlist(pluglist):
	global pluglistactive
	pluglistactive=pluglist

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


def imagealphaoff(filename):
	if (filename.lower()).endswith(".jpg") or (filename.lower()).endswith(".jpeg") or (filename.lower()).startswith("no-tr"):
		return 1
	else:
		return 0

dummyimage=pygame.Surface((48, 48))
dummyimage.fill((255, 0, 255))

def filelookup(filename):
	global filedict
	if filename in filedict:
		return filedict[filename]
	else:
		try:
			if imagealphaoff(filename):
				imgret=pygame.image.load(os.path.join(imagepath, filename)).convert()
				#print "noalpha"
			else:
				imgret=pygame.image.load(os.path.join(imagepath, filename)).convert_alpha()
				#print "alpha"
			filedict[filename]=imgret
			return imgret
		except pygame.error:
			for plug in pluglistactive:
				try:
					imgret=plug.imageloader(filename)
					if imgret!=None:
						return imgret
				except AttributeError:
					continue
	print("IMAGE FILENAME ERROR: nonvalid image filename. returning dummy image...")
	return dummyimage
		

#convienence function.
#give it a color, be it a rgb touple,
# html hex, or pygame color object, and it will always spit out a pygame color object.
def colorify(colorobj):
	if type(colorobj) is pygame.Color:
		return colorobj
	else:
		return pygame.Color(colorobj)


def textrender(text, size, fgcolor, bgcolor, transp):
	#ensure colors are pygame.Color objects
	fgcolor=colorify(fgcolor)
	bgcolor=colorify(bgcolor)
	#generate string forms of fg and bg colors for key.
	kfgcolor=str(fgcolor.r)+str(fgcolor.g)+str(fgcolor.b)
	kbgcolor=str(bgcolor.r)+str(bgcolor.g)+str(bgcolor.b)
	global textdict
	keyx=(text + str(size) + kfgcolor + kbgcolor + str(transp))
	if keyx in textdict:
		return textdict[keyx]
	else:
		
		texfnt=pygame.font.SysFont(None, size)
		if transp==0:
			texgfx=texfnt.render(text, True, fgcolor, bgcolor)
		else:
			texgfx=texfnt.render(text, True, fgcolor)
		textdict[keyx]=texgfx
		return texgfx

class clicktab:
	def __init__(self, box, reftype, ref, keyid, takekey, sfxclick, sound, quitab=0, data=None):
		self.box=box
		self.ref=ref
		self.keyid=keyid
		self.takekey=takekey
		self.reftype=reftype
		self.sfxclick=sfxclick
		self.sound=sound
		self.quitab=quitab
		self.data=data


def ctreport(box, selfref, dataval):
	return clicktab(box, 'report', selfref, '0', '0', 0, None, quitab=0, data=dataval)
	

def colorboost(colorobj, amnt):
	colorobj=colorify(colorobj)
	rcol=colorobj.r
	gcol=colorobj.g
	bcol=colorobj.b
	rcol+=amnt
	gcol+=amnt
	bcol+=amnt
	if rcol>255:
		rcol=255
	if rcol<0:
		rcol=0
	if gcol>255:
		gcol=255
	if gcol<0:
		gcol=0
	if bcol>255:
		bcol=255
	if bcol<0:
		bcol=0
	return pygame.Color(rcol, gcol, bcol)

def trace3dbox(surface, basecolor, rect, linewidth=1):
	basetint=colorboost(basecolor, 40)
	baseshad=colorboost(basecolor, -40)
	pygame.draw.line(surface, basetint, rect.topleft, rect.topright, linewidth)
	pygame.draw.line(surface, basetint, rect.topleft, rect.bottomleft, linewidth)
	pygame.draw.line(surface, baseshad, rect.bottomleft, rect.bottomright, linewidth)
	pygame.draw.line(surface, baseshad, rect.topright, rect.bottomright, linewidth)

def colorchanlimit(color):
		if color>255:
			return 255
		elif color<0:
			return 0
		else:
			return color
#non-alpha 2-color gradient function. outputs a 200x200 surface, use rotval 0 for no rotation.
#rotation values of non-90-degree increments will cause the returned surface to be LARGER than 200x200.
def makegradient(startcolor, endcolor, rotval):
	#print startcolor
	#print endcolor
	gradsurf = pygame.Surface((200, 200))
	startcolor = colorify(startcolor)
	endcolor = colorify(endcolor)
	#calculate float increment values for each color channel
	inccolorR = (startcolor.r - endcolor.r) / 200.0
	inccolorG = (startcolor.g - endcolor.g) / 200.0
	inccolorB = (startcolor.b - endcolor.b) / 200.0
	#initalize float color data storage values
	startcolorR = startcolor.r
	startcolorG = startcolor.g
	startcolorB = startcolor.b
	colcnt = 0
	#draw gradient
	while colcnt < 200:
		#draw horizontal line
		pygame.draw.line(gradsurf, startcolor, (0, colcnt), (200, colcnt))
		startcolorR -= inccolorR
		startcolorG -= inccolorG
		startcolorB -= inccolorB
		#update color channels
		startcolor.r = colorchanlimit(int(startcolorR))
		startcolor.g = colorchanlimit(int(startcolorG))
		startcolor.b = colorchanlimit(int(startcolorB))
		colcnt += 1
	if rotval==0:
		return gradsurf
	else:
		return pygame.transform.rotate(gradsurf, rotval)
			
