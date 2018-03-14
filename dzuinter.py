#!/usr/bin/env python
import pygame.event
import pygame.key
import pygame.display
import pygame.image
import pygame.mixer
from pygame.locals import *
import pygame
import sys
import time
import os
import dzulib1 as dzulib
from dzulib1 import textrender
pygame.display.init()
import traceback
import random
import xml.etree.ElementTree as ET
pluglist=[]


def OKpop(info, extra=None, extra2=None):
	screensurf=pygame.display.get_surface()
	bgrect=pygame.Rect(0, 0, screensurf.get_width()//1.8, 6*uitextsize)
	bgrect.centerx=(screensurf.get_width()//2)
	bgrect.centery=(screensurf.get_height()//2)
	pygame.draw.rect(screensurf, uibgcolor, bgrect)
	dzulib.trace3dbox(screensurf, uibgcolor, bgrect, 2)
	
	yoff=bgrect.y+2
	yjump=uitextsize
	#lineren=simplefont.render(info, True, (255, 255, 255), (30, 30, 30))
	lineren=textrender(info, uitextsize, uifgcolor, uibgcolor, 0)
	screensurf.blit(lineren, ((screensurf.get_width()//2)-(lineren.get_width()//2), yoff+0))
	yoff+=yjump
	if extra!=None:
		#lineren=simplefont.render(extra, True, (255, 255, 255), (30, 30, 30))
		lineren=textrender(extra, uitextsize, uifgcolor, uibgcolor, 0)
		screensurf.blit(lineren, ((screensurf.get_width()//2)-(lineren.get_width()//2), yoff+0))
		yoff+=yjump
	if extra2!=None:
		#lineren=simplefont.render(extra2, True, (255, 255, 255), (30, 30, 30))
		lineren=textrender(extra2, uitextsize, uifgcolor, uibgcolor, 0)
		screensurf.blit(lineren, ((screensurf.get_width()//2)-(lineren.get_width()//2), yoff+0))
		yoff+=yjump
	#lineren=simplefont.render("Press any key or click to continue", True, (255, 255, 255), (30, 30, 30))
	lineren=textrender("Press any key or click to continue", uitextsize, uifgcolor, uibgcolor, 0)
	screensurf.blit(lineren, ((screensurf.get_width()//2)-(lineren.get_width()//2), yoff+0))
	yoff+=yjump
	pygame.display.update()
	while True:
		time.sleep(0.1)
		for event in pygame.event.get():
			if event.type == QUIT:
				return
			if event.type == KEYDOWN:
				return
			if event.type==MOUSEBUTTONDOWN:
				return

def YNpop(info):
	screensurf=pygame.display.get_surface()
	bgrect=pygame.Rect(0, 0, screensurf.get_width()//1.8, 6*uitextsize)
	bgrect.centerx=(screensurf.get_width()//2)
	bgrect.centery=(screensurf.get_height()//2)
	pygame.draw.rect(screensurf, uibgcolor, bgrect)
	dzulib.trace3dbox(screensurf, uibgcolor, bgrect, 2)
	yoff=bgrect.y+2
	yjump=uitextsize
	#lineren=simplefont.render(info, True, (255, 255, 255), (30, 30, 30))
	lineren=textrender(info, uitextsize, uifgcolor, uibgcolor, 0)
	screensurf.blit(lineren, ((screensurf.get_width()//2)-(lineren.get_width()//2), yoff+0))
	yoff+=yjump
	#lineren=simplefont.render("(Y)es or (N)o?", True, (255, 255, 255), (30, 30, 30))
	lineren=textrender("        (Y)es        ", uitextsize, uifgcolor, dzulib.colorboost(uibgcolor, 40), 0)
	yesrect=screensurf.blit(lineren, ((screensurf.get_width()//2)-(lineren.get_width()//2), yoff+0))
	yoff+=yjump
	lineren=textrender("        (N)o        ", uitextsize, uifgcolor, dzulib.colorboost(uibgcolor, 40), 0)
	norect=screensurf.blit(lineren, ((screensurf.get_width()//2)-(lineren.get_width()//2), yoff+0))
	yoff+=yjump
	pygame.display.update()
	while True:
		time.sleep(0.1)
		for event in pygame.event.get():
			if event.type == QUIT:
				return 0
			if event.type == KEYDOWN and event.key == K_n:
				return 0
			if event.type == KEYDOWN and event.key == K_y:
				return 1
			if event.type==MOUSEBUTTONDOWN:
				if yesrect.collidepoint(event.pos):
					return 1
				if norect.collidepoint(event.pos):
					return 0

savepath="save"

def charremove(string, indexq):
	if indexq==0:
		return string
	else:
		return (string[:(indexq-1)] + string[(indexq):])
def charinsert(string, char, indexq):
	if indexq==0:
		return char + string
	else:
		return (string[:(indexq-1)] + char + string[(indexq-1):])



def fileselect(title):
	screensurf=pygame.display.get_surface()
	curoffset=0
	redraw=1
	textstring=""
	pathlist=sorted(os.listdir(os.path.join(savepath, '.')), key=str.lower)
	while True:
		time.sleep(0.1)
		if redraw==1:
			redraw=0
			yoff=2
			yjump=uitextsize+1
			bgrect=pygame.Rect(0, 50, screensurf.get_width()//2, screensurf.get_height())
			bgrect.centerx=(screensurf.get_width()//2)
			bgrect.centery=(screensurf.get_height()//2)
			yoff=bgrect.y+2
			pygame.draw.rect(screensurf, uibgcolor, bgrect)
			dzulib.trace3dbox(screensurf, uibgcolor, bgrect, 2)
			#pygame.draw.rect(screensurf, (255, 255, 255), bgrect, 1)
			#lineren=simplefont.render(title, True, (255, 255, 255), (30, 30, 30))
			lineren=textrender(title, uitextsize, uifgcolor, uibgcolor, 0)
			screensurf.blit(lineren, ((screensurf.get_width()//2)-(lineren.get_width()//2), yoff+50))
			yoff+=yjump
			linedict={}
			for line in pathlist:
				if line.endswith('.sav'):
					if line.split(".")[0]==textstring:
						lineren=textrender(line, uitextsize, uibgcolor, dzulib.colorboost(uifgcolor, 40), 0)
					else:
						lineren=textrender(line, uitextsize, uifgcolor, dzulib.colorboost(uibgcolor, 40), 0)
					bxrect=screensurf.blit(lineren, ((screensurf.get_width()//2)-(lineren.get_width()//2), yoff+50))
					yoff+=yjump
					linedict[line.split(".")[0]]=bxrect
			
			#abttextB=simplefont.render(textstring+".sav", True, (255, 255, 255), (40, 40, 40))
			abttextB=textrender(textstring+".sav", uitextsize, uibgcolor, dzulib.colorboost(uifgcolor, 40), 0)
			pygame.draw.line(screensurf, dzulib.colorboost(uibgcolor, 40), (bgrect.x, yoff+yjump*2), (bgrect.x+bgrect.w, yoff+yjump*2), 2)
			screensurf.blit(abttextB, (screensurf.get_width()//2-abttextB.get_width()//2, yoff+yjump*3))
			pygame.display.update()
		for event in pygame.event.get():
			if event.type==MOUSEBUTTONDOWN:
				for rectbx in linedict:
					if linedict[rectbx].collidepoint(event.pos):
						if rectbx==textstring:
							return rectbx+".sav"
						textstring=rectbx
						redraw=1
				if not bgrect.collidepoint(event.pos):
					return None
			if event.type == KEYDOWN and event.key == K_BACKSPACE:
				if len(textstring)!=0 and curoffset!=0:
					textstring=charremove(textstring, curoffset)
					curoffset -= 1
					redraw=1
				break
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				return None
			elif event.type == KEYDOWN and event.key == K_RETURN:
				if textstring!="":
					return textstring+ ".sav"
				else:
					OKpop("\".sav\" is not a valid name.")
					return None
			elif event.type == KEYDOWN and event.key != K_TAB:
				curoffset += 1
				textstring=charinsert(textstring, str(event.unicode), curoffset)
				redraw=1
				break
	