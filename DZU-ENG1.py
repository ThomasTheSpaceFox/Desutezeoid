#!/usr/bin/env python
import pygame.event
import pygame.key
import pygame.display
import pygame.image
import pygame.mixer
import pygame
import time
import os
import copy


# load dzulib1 Desutezeoid support library
import dzulib1 as dzulib
import dzupluglib
from dzulib1 import clicktab
from dzulib1 import textrender
from dzulib1 import filelookup
import dzuinter

from pygame.locals import *
import xml.etree.ElementTree as ET
pygame.display.init()
pygame.font.init()
pygame.mixer.init()
engversion="v1.7.1"
print("Desutezeoid arbitrary point and click engine " + engversion)
print("parsing ENGSYSTEM.xml")
conftree = ET.parse(os.path.join("xml", "ENGSYSTEM.xml"))
confroot = conftree.getroot()

screentag=confroot.find("screen")
plugcnftag=confroot.find("plugcnf")
uitag=confroot.find("ui")
uicolorstag=uitag.find("main")
uifgcolor=pygame.Color(uicolorstag.attrib.get("FGCOLOR", "#000000"))
uibgcolor=pygame.Color(uicolorstag.attrib.get("BGCOLOR", "#FFFFFF"))
uifgcolorstr=uicolorstag.attrib.get("FGCOLOR", "#000000")
uibgcolorstr=uicolorstag.attrib.get("BGCOLOR", "#FFFFFF")
uitextsize=int(uicolorstag.attrib.get("textsize", "24"))


dzuinter.uifgcolor=uifgcolor
dzuinter.uibgcolor=uibgcolor
dzuinter.uitextsize=uitextsize
uiquittag=uitag.find("quit")
uiquitmsg=uiquittag.attrib.get("MSG", "Are you sure you want to quit?")


pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP, KEYDOWN, KEYUP])



sfxpath='sfx'

imagepath='img'

			
savepath='save'

print("populate keylist with null keyid, add any keys in initkeys.")
initkeystag=confroot.find("initkeys")
savkeystag=confroot.find("savkeys")

keylist=list(["0"])
for initk in initkeystag.findall("k"):
	if (initk.attrib.get("keyid"))!="0":
		keylist.extend([initk.attrib.get("keyid")])


scrnx=int(screentag.attrib.get("x", "800"))
scrny=int(screentag.attrib.get("y", "600"))
titletag=confroot.find("title")
debugtag=confroot.find("debug")
DEBUG=int(debugtag.attrib.get("debug", "1"))
skipautoload=int(debugtag.attrib.get("skipautoload", "0"))
printkeys=int(debugtag.attrib.get("printkeys", "1"))
clickfields=int(debugtag.attrib.get("clickfields", "0"))
cfcolor=pygame.Color(debugtag.attrib.get("cfcolor", "#888888"))

beginref=(confroot.find("beginref")).text

globalcoretag=confroot.find("globalcore")
globalforkstag=confroot.find("globalforks")
icontag=titletag.attrib.get("icon", "NULL")
if icontag!="NULL":
	windowicon=pygame.image.load(os.path.join(imagepath, icontag))
	pygame.display.set_icon(windowicon)
	
print("config parsed.")
titlebase=titletag.attrib.get("base", "Desutezeoid: ")

class timeouttab:
	def __init__(self, seconds, keyid, postkey):
		self.keyid=keyid
		self.regtime=time.time()
		self.seconds=seconds
		self.postkey=postkey

class uimenutab:
	def __init__(self, con, keyid, stay=0, noact=0, surfrender=None):
		self.keyid=keyid
		self.con=con
		self.surfrender=surfrender
		self.stay=stay
		self.noact=noact




#class keyobj:
#	def __init__(self, keyid):
#		self=keyid
def debugmsg(msg):
	if DEBUG==1:
		print(msg)
def keyprint():
	if printkeys==1:
		print(keylist)
keyprint()
prevpage="NULL"
curpage=beginref

screensurf=pygame.display.set_mode((scrnx, scrny))
screensurf.set_alpha(None)
quitflag=0
clicklist=list()



pmenukey="0"
popkey="0"

#menu dialog function
def qmenu(xpos, ypos, itemlist, fgcol=uifgcolorstr, bgcol=uibgcolorstr, uipoptextsize=uitextsize):
	#qfnt=pygame.font.SysFont(None, uipoptextsize)
	texty=3
	textx=100
	fgc=dzulib.colorify(fgcol)
	bgc=dzulib.colorify(bgcol)
	bgbtn=dzulib.colorboost(bgcol, 40)
	itemlistB=list()
	for itm in itemlist:
		texty += uipoptextsize+3
		if itm.noact==1:
			#qtext1=qfnt.render(itm.con, True, fgcol, bgcol)
			qtext1=textrender(itm.con, uipoptextsize, fgcol, bgcol, 0)
		else:
			#qtext1=qfnt.render(itm.con, True, bgcol, fgcol)
			qtext1=textrender(itm.con, uipoptextsize, fgcol, bgbtn, 0)
		#print itm.con
		itmB=uimenutab(itm.con, itm.keyid, itm.stay, itm.noact, qtext1)
		if (qtext1.get_width()+4)>textx:
			textx=qtext1.get_width()+4
		itemlistB.extend([itmB])
	
	xpos=((xpos - int(textx / 2)) - 3)
	ypos=((ypos - int(texty / 2)) - 3)
	qboxwidth=(6 + textx)
	qboxhight=(texty + 20)
	if qboxwidth<100:
		qboxwidth=100
	qbox=pygame.Surface((qboxwidth, qboxhight))
	qbox.fill((bgc))
	boxtrace=screensurf.blit(qbox, (xpos, ypos))

	
	texreny=(ypos + 3)
	texrenx=(xpos + 3)
	retlist=list()
	for itm in itemlistB:
		texrenx=(xpos + (qboxwidth // 2) - (itm.surfrender.get_width()//2))
		
		#itmclick=screensurf.blit(itm.surfrender, (texrenx, (texreny)))
		itmclick=itm.surfrender.get_rect()
		itmclick.x = texrenx - 2
		itmclick.y = texreny - 2
		itmclick.w += 4
		itmclick.h += 4
		
		
		if itm.noact==0:
			pygame.draw.rect(screensurf, bgbtn, itmclick, 0)
			#pygame.draw.rect(screensurf, fgc, itmclick, 1)
			dzulib.trace3dbox(screensurf, bgc, itmclick, 1)
			screensurf.blit(itm.surfrender, (texrenx, (texreny)))
			if itm.stay==0:
				itmclicktab=clicktab(itmclick, "keym", "none", itm.keyid, "0", 0, "none", quitab=3)
			else:
				itmclicktab=clicktab(itmclick, "key", "none", itm.keyid, "0", 0, "none")
			retlist.extend([itmclicktab])
		else:
			screensurf.blit(itm.surfrender, (texrenx, (texreny)))
		texreny += uipoptextsize+3
	#screensurf.blit(qtext1, ((xpos + 3), (ypos + 3)))
	#pygame.draw.rect(screensurf, fgc, boxtrace, 3)
	dzulib.trace3dbox(screensurf, bgc, boxtrace, 3)
	return(retlist)

	


#simple dialog popup generator. used by uipop forks and the engine quit dialogs.
def qpop(qmsg, xpos, ypos, keyid="0", nokey="0", quyn=0, specialquit=0, fgcol=uifgcolorstr, bgcol=uibgcolorstr, uipoptextsize=uitextsize, img="none"):
	#qfnt=pygame.font.SysFont(None, uipoptextsize)
	fgc=dzulib.colorify(fgcol)
	bgc=dzulib.colorify(bgcol)
	bgbtn=dzulib.colorboost(bgcol, 40)
	if img!="none":
		qimg=filelookup(img)
		qimgflg=1
		qimgy=qimg.get_height()
		qimgx=qimg.get_width()
	else:
		qimgflg=0
		qimgy=0
		qimgx=0
	prevxpos=xpos
	#qtext1=qfnt.render(qmsg, True, fgcol, bgcol)
	qtext1=textrender(qmsg, uipoptextsize, fgcol, bgcol, 0)
	xpos=((xpos - int(qtext1.get_width() / 2)) - 3)
	if qimgflg==1:
		#if image is present, center ypos on image
		ypos=((ypos - int(qimgy / 2)))
	qboxwidth=(6 + (qtext1.get_width()))
	qboxhight=(uipoptextsize + qimgy + uipoptextsize + 20)
	if qboxwidth<200:
		qboxwidth=200
	if qboxwidth<qimgx:
		qboxwidth=(qimgx + 6)
		#if image is wider than text, center xpos on image
		xpos=((prevxpos - int(qimgx / 2)) - 3)
	qbox=pygame.Surface((qboxwidth, qboxhight))
	qbox.fill((bgc))
	boxtrace=screensurf.blit(qbox, (xpos, ypos))
	if qimgflg==1:
		screensurf.blit(qimg, ((xpos + qboxwidth//2-qimg.get_width()//2), (ypos + 3)))
	screensurf.blit(qtext1, ((xpos + qboxwidth//2-qtext1.get_width()//2), (ypos + qimgy + 3)))
	#pygame.draw.rect(screensurf, fgc, boxtrace, 3)
	dzulib.trace3dbox(screensurf, bgc, boxtrace, 3)
	if quyn==1:
		#qytext=qfnt.render("Yes", True, bgcol, fgcol)
		#qntext=qfnt.render("No", True, bgcol, fgcol)
		qytext=textrender("Yes", uipoptextsize, fgcol, bgbtn, 0)
		qntext=textrender("No", uipoptextsize, fgcol, bgbtn, 0)
		yesclick=qytext.get_rect()
		noclick=qntext.get_rect()
		yesclick.w += 4
		yesclick.h += 4
		if yesclick.w<80:
			yesclick.w=80
		yesclick.x =(xpos + qboxwidth//2 - yesclick.w//2 - 60)
		yesclick.y =(ypos + qimgy + 10 - 2 + uipoptextsize)
		
		noclick.w += 4
		noclick.h += 4
		if noclick.w<80:
			noclick.w=80
		noclick.x =(xpos + qboxwidth//2 - noclick.w//2 + 60)
		noclick.y =(ypos + qimgy + 10 - 2 + uipoptextsize)
		
		pygame.draw.rect(screensurf, bgbtn, noclick, 0)
		dzulib.trace3dbox(screensurf, bgc, noclick, 1)
		screensurf.blit(qntext, (noclick.x+noclick.w//2-qntext.get_width()//2, noclick.y+2))
		pygame.draw.rect(screensurf, bgbtn, yesclick, 0)
		dzulib.trace3dbox(screensurf, bgc, yesclick, 1)
		screensurf.blit(qytext, (yesclick.x+yesclick.w//2-qytext.get_width()//2, yesclick.y+2))
		#yesclick=screensurf.blit(qytext, ((xpos + 10), (ypos + qimgy + 10 + uipoptextsize)))
		#noclick=screensurf.blit(qntext, ((xpos + 50), (ypos + qimgy + 10 + uipoptextsize)))
		ref="none"
		takekey="0"
		clicksoundflg=0
		soundname=0
		if specialquit==1:
			yesdat=clicktab(yesclick, "quitx", ref, keyid, takekey, clicksoundflg, soundname)
			nodat=clicktab(noclick, "key", ref, nokey, takekey, clicksoundflg, soundname, quitab=1)
		else:
			yesdat=clicktab(yesclick, "keyx", ref, keyid, takekey, clicksoundflg, soundname, quitab=2)
			nodat=clicktab(noclick, "keyx", ref, nokey, takekey, clicksoundflg, soundname, quitab=2)
		retclicks=([])
		retclicks.extend([yesdat])
		retclicks.extend([nodat])

		return(retclicks, quyn)
	else:
		#qytext=qfnt.render("Ok", True, bgcol, fgcol)
		qytext=textrender("Ok", uipoptextsize, fgcol, bgbtn, 0)
		yesclick=qytext.get_rect()
		yesclick.w += 4
		yesclick.h += 4
		if yesclick.w<80:
			yesclick.w=80
		yesclick.x =(xpos + qboxwidth//2 - yesclick.w//2)
		yesclick.y =(ypos + qimgy + 10 - 2 + uipoptextsize)
		
		pygame.draw.rect(screensurf, bgbtn, yesclick, 0)
		dzulib.trace3dbox(screensurf, bgc, yesclick, 1)
		screensurf.blit(qytext, (yesclick.x+yesclick.w//2-qytext.get_width()//2, yesclick.y+2))
		
		#yesclick=screensurf.blit(qytext, ((xpos + 10), (ypos + qimgy + 10 + uipoptextsize)))
		ref="none"
		takekey="0"
		clicksoundflg=0
		soundname=0
		yesdat=clicktab(yesclick, "keyx", ref, keyid, takekey, clicksoundflg, soundname, quitab=2)
		retclicks=([])
		retclicks.extend([yesdat])
		return(retclicks, quyn)

class vartreeclass:
	def __init__(self):
		self.curpage=curpage
		self.uifgcolorstr=uifgcolorstr
		self.uibgcolorstr=uibgcolorstr
		self.uitextsize=uitextsize
		self.engversion=engversion


vartree=vartreeclass()
pluglistactive=[]

for pluginst in dzupluglib.pluglist:
	print("loading: " + pluginst.plugname)
	pluglistactive.extend([pluginst.plugclass(screensurf, keylist, vartree)])
dzulib.definepluginlist(pluglistactive)
for cnfplug in plugcnftag.findall("*"):
	for pluginst in pluglistactive:
		try:
			pluginst.cnfload(cnfplug)
		except AttributeError:
			continue





def pause(crash=False):
	pausestart=time.time()
	for plug in pluglistactive:
		try:
			plug.pause(pausestart)
		except AttributeError:
			continue
	noexit=1
	pygame.mixer.pause()
	pygame.mixer.music.pause()
	scbak=screensurf.copy()
	halfwidth=screensurf.get_width()//2
	halfheight=screensurf.get_height()//2
	subback=pygame.transform.scale(scbak, (halfwidth, halfheight))
	buttonwidth=halfwidth//1.2
	buttonheight=uitextsize+6
	dispu=1
	menulist=["Resume", "Load...", "Save...", "New Game", "Quit"]
	renmenu=[]
	for mnu in menulist:
		rentext=textrender(mnu, uitextsize, uifgcolor, dzulib.colorboost(uibgcolor, 40), 0)
		btnsurf=pygame.Surface((buttonwidth, buttonheight))
		btnsurf.fill(dzulib.colorboost(uibgcolor, 40))
		btnsurf.blit(rentext, (buttonwidth//2-rentext.get_width()//2, buttonheight//2-rentext.get_height()//2))
		dzulib.trace3dbox(btnsurf, uibgcolor, pygame.Rect(0, 0, buttonwidth-1, buttonheight-1))
		renmenu.extend([btnsurf])
	pausetext=textrender("Game Paused.", uitextsize, uifgcolor, uibgcolor, 0)
	pausetext2=textrender("Powered By: Desutezeoid " + str(vartree.engversion), uitextsize, uifgcolor, uibgcolor, 0)
	pausetext3=textrender("Copyright (c) 2015-2018 Thomas Leathers and Contributors", uitextsize, uifgcolor, uibgcolor, 0)
	pausetext4=textrender("A point and click adventure game engine. See DZU_README.md", uitextsize, uifgcolor, uibgcolor, 0)
	retact=None
	while noexit:
		if dispu:
			dispu=0
			screensurf.fill(uibgcolor)
			screensurf.blit(pausetext, (10, 10))
			screensurf.blit(pausetext2, (10, screensurf.get_height()-uitextsize*3))
			screensurf.blit(pausetext3, (10, screensurf.get_height()-uitextsize*2))
			screensurf.blit(pausetext4, (10, screensurf.get_height()-uitextsize))
			menuy=buttonheight+4
			rectmenu=[]
			for mnu in renmenu:
				rectmenu.extend([screensurf.blit(mnu, (10, menuy))])
				menuy+=buttonheight+4
			
			subbackrect=screensurf.blit(subback, (halfwidth-3, 3))
			dzulib.trace3dbox(screensurf, uibgcolor, subbackrect, 2)
		pygame.display.update()
		time.sleep(0.1)
		for event in pygame.event.get():
			if event.type==MOUSEBUTTONDOWN:
				if rectmenu[0].collidepoint(event.pos):
					noexit=0
					break
				if rectmenu[1].collidepoint(event.pos):
					dispu=1
					selret=dzuinter.fileselect("load...")
					if selret!=None:
						retact=["load", selret]
						noexit=0
						break
				if rectmenu[2].collidepoint(event.pos):
					dispu=1
					selret=dzuinter.fileselect("save...")
					if selret!=None:
						if selret=="autosave.sav":
							dzuinter.OKpop("file \"autosave.sav\" is used for autosave.")
						elif os.path.isfile(os.path.join(savepath, selret)):
							if dzuinter.YNpop("file \"" + selret + "\" exists. overwrite?"):
								retact=["save", selret]
								noexit=0
								break
						else:
							retact=["save", selret]
							noexit=0
							break
				if rectmenu[3].collidepoint(event.pos):
					dispu=1
					if dzuinter.YNpop("Start a new game? Unsaved Progress will be lost!"):
						noexit=0
						retact=["newgame"]
						break
				if rectmenu[4].collidepoint(event.pos):
					noexit=0
					retact=["quit"]
					break
			if event.type==KEYDOWN:
				if event.key == K_ESCAPE:
					noexit=0
					break
	pygame.mixer.unpause()
	pygame.mixer.music.unpause()
	pausestop=time.time()-pausestart
	for f in timeoutlist:
		f.seconds+=pausestop
	for plug in pluglistactive:
		try:
			plug.resume(pausestop)
		except AttributeError:
			continue
	return retact

def saver(savefile="autosave.sav"):
	global keysav
	print("saving... Please Wait.")
	#clear keysav section.
	for savk in keysav.findall("*"):
		keysav.remove(savk)
	#print(ET.tostring(mainsavroot).decode())
	for savk in list(set(keylist)):
		#keysav.append(copy.deepcopy(savk))
		savelem=ET.SubElement(keysav, 'k')
		savelem.set("keyid", savk)
	if pmenukey!="0":
		savelem=ET.SubElement(keysav, 'k')
		savelem.set("keyid", pmenukey)
	if popkey!="0":
		savelem=ET.SubElement(keysav, 'k')
		savelem.set("keyid", popkey)
	for pluginst in pluglistactive:
		try:
			pluginst.savwrite(plugsavtag)
		except AttributeError:
			continue
	if pygame.mixer.music.get_busy() and BGMtrack!=None:
		
		mainsavroot.find('pagelink').set("musictrack", BGMtrack)
	else:
		mainsavroot.find('pagelink').set("musictrack", "??none??")
	#save page refrence
	mainsavroot.find('pagelink').set("page", vartree.curpage)
	mainsavtree.write(os.path.join(savepath, savefile))
saveload=0
#load main.sav. if IOError, Attempt to initalize main.sav, then try to load main.sav again.
def loader(savefile="autosave.sav", returnonerror=0):
	global mainsavtree
	global mainsavroot
	global plugsavtag
	global keysav
	global keylist
	global saveload
	global BGMtrack
	try:
		mainsavtree = ET.parse(os.path.join(savepath, savefile))
		mainsavroot = mainsavtree.getroot()
		del keylist[:]
		print(".sav loaded")
		pagelink=mainsavroot.find('pagelink').attrib.get("page")
		BGMtrack=mainsavroot.find('pagelink').attrib.get("musictrack")
		if BGMtrack=="??none??":
			BGMtrack=None
		pygame.mixer.music.stop()
		if BGMtrack!=None:
			
			pygame.mixer.music.load(os.path.join(sfxpath, BGMtrack))
			pygame.mixer.music.play(-1)
		
		if pagelink!=None:
			prevpage="NULL"
			vartree.curpage=pagelink
		plugsavtag=mainsavroot.find('plugsav')
		saveload=1
		for pluginst in pluglistactive:
			try:
				pluginst.savload(plugsavtag)
			except AttributeError:
				continue
		print("add any keyids from .sav")
		keysav=mainsavroot.find('keysav')
		for savk in keysav.findall("k"):
			if (savk.attrib.get("keyid"))!="0":
				if savk.attrib.get("keyid") not in keylist:
					keylist.extend([savk.attrib.get("keyid")])
		#for initk in initkeystag.findall("k"):
		#	if (initk.attrib.get("keyid"))!="0":
		#		if initk.attrib.get("keyid") not in keylist:
		#			keylist.extend([initk.attrib.get("keyid")])
		if "0" not in keylist:
			keylist.extend(["0"])
	except IOError:
		if returnonerror==1:
			return
		print ('.sav not found.')
		dzulib.initmainsave()
		mainsavtree = ET.parse(os.path.join(savepath, savefile))
		mainsavroot = mainsavtree.getroot()
		keysav=mainsavroot.find('keysav')
		print(".sav loaded")
		plugsavtag=mainsavroot.find('plugsav')
		BGMtrack=None
		for pluginst in pluglistactive:
			try:
				pluginst.savload(plugsavtag)
			except AttributeError:
				continue
		del keylist[:]
		for initk in initkeystag.findall("k"):
			if (initk.attrib.get("keyid"))!="0":
				keylist.extend([initk.attrib.get("keyid")])
		if "0" not in keylist:
			keylist.extend(["0"])

def newgame():
	print("starting new game... please wait...")
	global mainsavtree
	global mainsavroot
	global plugsavtag
	global keysav
	global keylist
	global prevpage
	global BGMtrack
	pygame.mixer.music.stop()
	BGMtrack=None
	dzulib.initmainsave()
	mainsavtree = ET.parse(os.path.join(savepath, "autosave.sav"))
	mainsavroot = mainsavtree.getroot()
	#return to beginref
	vartree.curpage=beginref
	prevpage="NULL"
	keysav=mainsavroot.find('keysav')
	print(".sav loaded")
	plugsavtag=mainsavroot.find('plugsav')
	
	for pluginst in pluglistactive:
		try:
			pluginst.savload(plugsavtag)
		except AttributeError:
			continue
	del keylist[:]
	for initk in initkeystag.findall("k"):
		if (initk.attrib.get("keyid"))!="0":
			keylist.extend([initk.attrib.get("keyid")])
	if "0" not in keylist:
		keylist.extend(["0"])
if not skipautoload:
	loader()
else:
	newgame()
	

timeoutlist=list()
keybak=list(keylist)
forksanitycheck=0
forksanity=0
cachepage=prevpage
print("done. begin mainloop.")
uiquit=0
qpopflg=0
qmenuflg=0

engtimer=pygame.time.Clock()
while quitflag==0:
	huris=0
	clicklist=list()
	#Engine Speed
	#time.sleep(0.05)
	engtimer.tick(30)
	pos = pygame.mouse.get_pos()
	#print "tic"
	if vartree.curpage!=prevpage:
		print("flushing image cache")
		del dzulib.filedict
		dzulib.filedict={}
		del dzulib.textdict
		dzulib.textdict={}
		print("notify plugins of page change")
		for pluginst in pluglistactive:
			pluginst.pageclear()
		print("preparsing page")
		tree = ET.parse(os.path.join("xml", vartree.curpage))
		root = tree.getroot()
		cachepage=prevpage
		prevpage=vartree.curpage
		coretag=root.find('core')
		forktag=root.find('forks')
		print("parsing global core objects into page structure...")
		for glb in globalcoretag:
			coretag.append(copy.deepcopy(glb))
		print("parsing global fork objects into page structure...")
		for glb in globalforkstag:
			forktag.append(copy.deepcopy(glb))
		pageconf=root.find('pageconf')
		pagetitle=(pageconf.find('title')).text
		BGMstop=int(pageconf.attrib.get("BGMstop", "1"))
		pagekeysflg=int(pageconf.attrib.get("pagekeys", "0"))
		if pagekeysflg==1 and saveload==0:
			pagekeytag=root.find("pagekeys")
			for pagekey in pagekeytag.findall("k"):
				pagekeyid=pagekey.attrib.get("keyid")
				if not pagekeyid in keylist:
					keylist.extend([pagekeyid])
					#print keylist
					keyprint()
		if BGMstop==1 and saveload==0:
			pygame.mixer.music.stop()
		BGon=int(pageconf.attrib.get("BGimg", "0"))
		BGMon=int(pageconf.attrib.get("BGM", "0"))
		if BGMon==1 and saveload==0:
			BGMtrack=(pageconf.find('BGM')).text
			pygame.mixer.music.load(os.path.join(sfxpath, BGMtrack))
			pygame.mixer.music.play(-1)
		pygame.display.set_caption((titlebase + pagetitle), (titlebase + pagetitle))
		print(("Page title: '" + pagetitle + "'"))
		if BGon==1:
			BGfile=(pageconf.find('BG')).text
			BG=pygame.image.load(os.path.join(imagepath, BGfile)).convert()
		screensurf.fill((170, 170, 170))
		saveload=0
		print("done. begin mainloop")
	if BGon==1:
		screensurf.blit(BG, (0, 0))
	for fork in forktag.findall("*"):
		#new game
		if fork.tag==("newgame"):
			masterkey=fork.attrib.get("keyid")
			if masterkey in keylist:
				keylist.remove(masterkey)
				#dzulib.initmainsave()
				newgame()
		if fork.tag==("ortrig"):
			#print "batchtrig"
			masterkey=fork.attrib.get("keyid")
			orflg=0
			for keyif in fork.findall("k"):
				ifpol=keyif.attrib.get("if")
				subkey=keyif.attrib.get("keyid")
				if subkey in keylist:
					if ifpol=="1":
						orflg=1
				elif not subkey in keylist:
					if ifpol=="0":
						orflg=1
			if orflg == 1:
				if not masterkey in keylist:
					keylist.extend([masterkey])
					#print keylist
					keyprint()
					forksanity=1
			else:
				if masterkey in keylist:
					keylist.remove(masterkey)
					#print keylist
					keyprint()
					forksanity=1
		
		if fork.tag==("batchtrig"):
			#print "batchtrig"
			masterkey=fork.attrib.get("keyid")
			complist=[1] 
			for keyif in fork.findall("k"):
				ifpol=keyif.attrib.get("if")
				subkey=keyif.attrib.get("keyid")
				if subkey in keylist:
					if ifpol=="1":
						complist.extend([1])
					else:
						complist.extend([0])
				elif not subkey in keylist:
					if ifpol=="0":
						complist.extend([1])
					else:
						complist.extend([0])
			if len(set(complist)) == 1:
				if not masterkey in keylist:
					keylist.extend([masterkey])
					#print keylist
					keyprint()
					forksanity=1
			else:
				if masterkey in keylist:
					keylist.remove(masterkey)
					#print keylist
					keyprint()
					forksanity=1
		if fork.tag==("batchset"):
			#print "batch"
			#print fork
			masterkey=fork.attrib.get("keyid")
			toggpol=fork.attrib.get("set")
			if masterkey in keylist:
				keylist.remove(masterkey)
				if toggpol=="1":
					for subkey in fork.findall("k"):
						subkeyid=subkey.attrib.get("keyid")
						if not subkeyid in keylist:
							keylist.extend([subkeyid])
							#print keylist
							keyprint()
					forksanity=1
				elif toggpol=="2":
					for subkey in fork.findall("k"):
						subkeyid=subkey.attrib.get("keyid")
						if not subkeyid in keylist:
							keylist.extend([subkeyid])
							#print keylist
							keyprint()
						elif subkeyid in keylist:
							keylist.remove(subkeyid)
							#print keylist
							keyprint()
				else:
					for subkey in fork.findall("k"):
						subkeyid=subkey.attrib.get("keyid")
						if subkeyid in keylist:
							keylist.remove(subkeyid)
							#print keylist
							keyprint()
					forksanity=1
		pagejumpflag=0
		if fork.tag==("pagejump"):
			masterkey=fork.attrib.get("keyid")
			if masterkey in keylist:
				keylist.remove(masterkey)
				useprvpge=int(fork.attrib.get('useprev', '0'))
				vartree.curpage=fork.attrib.get("page")
				if useprvpge==1 and cachepage!="NULL":
					vartree.curpage=cachepage
					
				
				print(("iref: loading page '" + vartree.curpage + "'"))
				pagejumpflag=1
				break
		if fork.tag==("music"):
			masterkey=fork.attrib.get("keyid")
			if masterkey in keylist:
				keylist.remove(masterkey)
				xmusstop=int(fork.attrib.get('stop', '0'))
				xmusplay=int(fork.attrib.get('play', '0'))
				if xmusstop==1:
					pygame.mixer.music.stop()
				elif xmusplay==1:
					try:
						pygame.mixer.music.play(-1)
					except pygame.error:
						debugmsg("ERROR: music fork play syntax used, but no music tracks were loaded. \n perhaps use the music track change syntax?")
				else:
					mustrack=fork.attrib.get("track")
					pygame.mixer.music.load(os.path.join(sfxpath, mustrack))
					pygame.mixer.music.play(-1)
				
		if fork.tag==("uipop"):
			masterkey=fork.attrib.get("keyid")
			msg=fork.attrib.get("msg")
			qpopx=int(fork.attrib.get("x",(screensurf.get_rect().centerx)))
			qpopy=int(fork.attrib.get("y",(screensurf.get_rect().centery)))
			#FGCOL=pygame.Color(fork.attrib.get("FGCOLOR", vartree.uifgcolorstr))
			#BGCOL=pygame.Color(fork.attrib.get("BGCOLOR", vartree.uibgcolorstr))
			FGCOL=fork.attrib.get("FGCOLOR", vartree.uifgcolorstr)
			BGCOL=fork.attrib.get("BGCOLOR", vartree.uibgcolorstr)
			QFNTSIZE=int(fork.attrib.get("textsize", vartree.uitextsize))
			uiimg=fork.attrib.get("img", "none")
	
			if masterkey in keylist:
				keylist.remove(masterkey)
				popkey=masterkey
				ynflag=int(fork.attrib.get("ynflag", "0"))
				if ynflag==1:
					yeskey=fork.attrib.get("yeskey", "0")
					nokey=fork.attrib.get("nokey", "0")
					#poppost=qpop(msg, qpopx, qpopy, keyid=yeskey, nokey=nokey, quyn=1)
					qpopdat=(msg, qpopx, qpopy, yeskey, nokey, 1, FGCOL, BGCOL, QFNTSIZE, uiimg)
					qpopflg=1
				else:
					okkey=fork.attrib.get("okkey", "0")
					#poppost=qpop(msg, qpopx, qpopy, keyid=okkey, quyn=0)
					qpopdat=(msg, qpopx, qpopy, okkey, "0", 0, FGCOL, BGCOL, QFNTSIZE, uiimg)
					qpopflg=1
					
		if fork.tag==("uimenu"):
			masterkey=fork.attrib.get("keyid")
			qpopx=int(fork.attrib.get("x",(screensurf.get_rect().centerx)))
			qpopy=int(fork.attrib.get("y",(screensurf.get_rect().centery)))
			#FGCOL=pygame.Color(fork.attrib.get("FGCOLOR", vartree.uifgcolorstr))
			#BGCOL=pygame.Color(fork.attrib.get("BGCOLOR", vartree.uibgcolorstr))
			FGCOL=fork.attrib.get("FGCOLOR", vartree.uifgcolorstr)
			BGCOL=fork.attrib.get("BGCOLOR", vartree.uibgcolorstr)
			QFNTSIZE=int(fork.attrib.get("textsize", vartree.uitextsize))
			if masterkey in keylist:
				pmenukey=masterkey
				keylist.remove(masterkey)
				itemlist=list()
				for itmf in fork.findall("item"):
					itmftab=uimenutab(itmf.attrib.get("con"), itmf.attrib.get("keyid", "0"), stay=int(itmf.attrib.get("stay", "0")), noact=int(itmf.attrib.get("noact", "0")))
					itemlist.extend([itmftab])
				qmenudat=(qpopx, qpopy, itemlist, FGCOL, BGCOL, QFNTSIZE)
				qmenuflg=1
		if fork.tag==("timeout"):
			masterkey=fork.attrib.get("keyid")
			if masterkey in keylist:
				notinlist=1
				for tif in timeoutlist:
					if tif.keyid==masterkey:
						notinlist=0
				if notinlist==1:
					seconds=float(fork.attrib.get("seconds"))
					postkey=fork.attrib.get("post", "0")
					timeoutlist.extend([timeouttab(seconds, masterkey, postkey)])
		if fork.tag==("triggerlock"):
			masterkey=fork.attrib.get("keyid")
			triggerkey=fork.attrib.get("trigger")
			lockkey=fork.attrib.get("lock")
			if masterkey in keylist:
				#keylist.remove(masterkey)
				if lockkey not in keylist:
					if triggerkey not in keylist:
						keylist.extend([triggerkey])
						keylist.extend([lockkey])
		
					
		if fork.tag==("sound"):
			masterkey=fork.attrib.get("keyid")
			soundname=fork.attrib.get("sound")
			if masterkey in keylist:
				keylist.remove(masterkey)
				soundobj=pygame.mixer.Sound(os.path.join(sfxpath, soundname))
				soundobj.play()
		#plugin parser
		for pluginst in pluglistactive:
			pluginst.fork(fork)
	
	if forksanity==1:
		forksanitycheck=1
		forksanity=0
		#skiploop=1
	else:
		forksanitycheck=0
	
	for tif in timeoutlist:
		if tif.keyid not in keylist:
			
			timeoutlist.remove(tif)
		elif ((time.time()) - tif.regtime) > tif.seconds:
			keylist.remove(tif.keyid)
			if tif.postkey not in keylist:
				if tif.postkey!="0":
					keylist.extend([tif.postkey])
			#print keylist
			keyprint()
			timeoutlist.remove(tif)		
		
	keybak=list(keylist)
	#print keylist
	#core object render-parser
	for labref in coretag.findall("*"):
		if labref.tag=="img":
			keyid=labref.attrib.get('keyid', "0")
			takekey=labref.attrib.get('takekey', "0")
			onkey=labref.attrib.get('onkey', "0")
			offkey=labref.attrib.get('offkey', "0")
			hoverkey=labref.attrib.get('hoverkey', "0")
			clicksoundflg=int(labref.attrib.get('sfxclick', "0"))
			soundname=(labref.attrib.get('sound', "0"))
			vscrollval=float(labref.attrib.get('vscroll', "0"))
			hscrollval=float(labref.attrib.get('hscroll', "0"))
			vscfl=int(labref.attrib.get('vscINT', "0"))
			hscfl=int(labref.attrib.get('hscINT', "0"))
			folmousehflg=int(labref.attrib.get('mouseh', "0"))
			folmousevflg=int(labref.attrib.get('mousev', "0"))
			if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
				imgx=int(labref.attrib.get("x"))
				imgy=int(labref.attrib.get("y"))
				imgcon=(labref.find("con")).text
				hovpic=int(labref.attrib.get("hovpic", "0"))
				act=labref.find("act")
				acttype=act.attrib.get("type", "none")
				pos = pygame.mouse.get_pos()
				#scrolling operation init code. (variables are stored inside xml tree in ram)
				if vscfl==0 and vscrollval!=0:
					vscfl=1
					labref.set('vscINT', "1")
					labref.set('vscINTOF', str(vscrollval))
				if hscfl==0 and hscrollval!=0:
					hscfl=1
					labref.set('hscINT', "1")
					labref.set('hscINTOF', str(hscrollval))
				vscoffset=float(labref.attrib.get('vscINTOF', "0"))
				hscoffset=float(labref.attrib.get('hscINTOF', "0"))
				imggfx=filelookup(imgcon)
				if folmousehflg==1:
					imgx=pos[0]
				if folmousevflg==1:
					imgy=pos[1]
				if folmousehflg==2:
					imgx=(pos[0] - int(imggfx.get_width() / 2))
				if folmousevflg==2:
					imgy=(pos[1] - int(imggfx.get_height() / 2))
				if folmousehflg==3:
					moux1=(abs(pos[0] - screensurf.get_width()) - int(imggfx.get_width() / 2))
					imgx=moux1
					#print "x" + str(imgx)
				if folmousevflg==3:
					mouy1=(abs(pos[1] - screensurf.get_height()) - int(imggfx.get_height() / 2))
					imgy=mouy1
					#print "y" + str(imgy)
				if vscfl==1:
					vscoffset += vscrollval
					if imggfx.get_height()<vscoffset:
						vscoffset=0
					if imggfx.get_height()<(vscoffset * -1):
						vscoffset=0
					labref.set('vscINTOF', str(vscoffset))
				if hscfl==1:
					hscoffset += hscrollval
					if imggfx.get_width()<hscoffset:
						hscoffset=0
					if imggfx.get_width()<(hscoffset * -1):
						hscoffset=0
					labref.set('hscINTOF', str(hscoffset))
				#imggfx=pygame.image.load(imgcon)
				
				if hscfl==1:
					imggfx=dzulib.hscroll(int(hscoffset), imggfx)
				if vscfl==1:
					imggfx=dzulib.vscroll(int(vscoffset), imggfx)
				#clickref=screensurf.blit(imggfx, (imgx, imgy))
				clickref=imggfx.get_rect()
				clickref.x=imgx
				clickref.y=imgy
				if hoverkey!="0":
					if clickref.collidepoint(pos)==1:
						if not hoverkey in keylist:
							keylist.extend([hoverkey])
					else:
						if hoverkey in keylist:
							keylist.remove(hoverkey)
				if hovpic==1:
					hovcon=(labref.find("altcon")).text
					hovgfx=filelookup(hovcon)
					if clickref.collidepoint(pos)==1:
						clickref=screensurf.blit(hovgfx, (imgx, imgy))
					else:
						clickref=screensurf.blit(imggfx, (imgx, imgy))
				else:
					clickref=screensurf.blit(imggfx, (imgx, imgy))
				if acttype!="none":
					pos = pygame.mouse.get_pos()
					if acttype=="iref":
						ref=act.attrib.get("ref")
						datstr=clicktab(clickref, "iref", ref, keyid, takekey, clicksoundflg, soundname)
						clicklist.extend([datstr])
					if acttype=="prev":
						ref=act.attrib.get("ref")
						datstr=clicktab(clickref, "prev", ref, keyid, takekey, clicksoundflg, soundname)
						clicklist.extend([datstr])
					if acttype=="quit":
						ref=act.attrib.get("ref")
						datstr=clicktab(clickref, "quit", ref, keyid, takekey, clicksoundflg, soundname)
						clicklist.extend([datstr])
					if acttype=="key":
						ref=act.attrib.get("ref")
						datstr=clicktab(clickref, "key", ref, keyid, takekey, clicksoundflg, soundname)
						clicklist.extend([datstr])
		if labref.tag=="box":
			keyid=labref.attrib.get('keyid', "0")
			takekey=labref.attrib.get('takekey', "0")
			onkey=labref.attrib.get('onkey', "0")
			offkey=labref.attrib.get('offkey', "0")
			hoverkey=labref.attrib.get('hoverkey', "0")
			clicksoundflg=int(labref.attrib.get('sfxclick', "0"))
			soundname=(labref.attrib.get('sound', "0"))
			if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
				imgx=int(labref.attrib.get("x"))
				imgy=int(labref.attrib.get("y"))
				sizex=int(labref.attrib.get("sizex"))
				sizey=int(labref.attrib.get("sizey"))
				onhov=int(labref.attrib.get("onhov", "0"))
				hovcolor=pygame.Color(labref.attrib.get("HOVCOLOR", "#FFFFFF"))
				hovalpha=int(labref.attrib.get("hovalpha", "140"))
				boxalpha=int(labref.attrib.get("alpha", "100"))
				boxcolor=pygame.Color(labref.attrib.get("COLOR", "#FFFFFF"))
				#imgcon=(labref.find("con")).text
				act=labref.find("act")
				acttype=act.attrib.get("type", "none")
				pos = pygame.mouse.get_pos()
				#imggfx=pygame.image.load(imgcon)
				boxgfx=pygame.Surface((sizex, sizey))
				boxgfx.convert_alpha()
				#imggfx.fill(boxcolor)
				boxgfx.set_alpha(0)
				clickref=screensurf.blit(boxgfx, (imgx, imgy))
				if onhov==1 and clickref.collidepoint(pos)==1:
					
					#skip blitting a second time if alpha is 0.
					if hovalpha!=0:
						boxgfx.fill(hovcolor)
						boxgfx.set_alpha(hovalpha)
						clickref=screensurf.blit(boxgfx, (imgx, imgy))
				else:
					
					#skip blitting a second time if alpha is 0.
					if boxalpha!=0:
						boxgfx.fill(boxcolor)
						boxgfx.set_alpha(boxalpha)
						clickref=screensurf.blit(boxgfx, (imgx, imgy))
				if hoverkey!="0":
					if clickref.collidepoint(pos)==1:
						if not hoverkey in keylist:
							keylist.extend([hoverkey])
					else:
						if hoverkey in keylist:
							keylist.remove(hoverkey)		
				if acttype!="none":
					pos = pygame.mouse.get_pos()
					if acttype=="iref":
						ref=act.attrib.get("ref")
						datstr=clicktab(clickref, "iref", ref, keyid, takekey, clicksoundflg, soundname)
						clicklist.extend([datstr])
					if acttype=="prev":
						ref=act.attrib.get("ref")
						datstr=clicktab(clickref, "prev", ref, keyid, takekey, clicksoundflg, soundname)
						clicklist.extend([datstr])
					if acttype=="quit":
						ref=act.attrib.get("ref")
						datstr=clicktab(clickref, "quit", ref, keyid, takekey, clicksoundflg, soundname)
						clicklist.extend([datstr])
					if acttype=="key":
						ref=act.attrib.get("ref")
						datstr=clicktab(clickref, "key", ref, keyid, takekey, clicksoundflg, soundname)
						clicklist.extend([datstr])
		if labref.tag=="text":
			onkey=labref.attrib.get('onkey', "0")
			offkey=labref.attrib.get('offkey', "0")
			if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
				labx=int(labref.attrib.get("x"))
				laby=int(labref.attrib.get("y"))
				size=int(labref.attrib.get("size"))
				#FGCOL=pygame.Color(labref.attrib.get("FGCOLOR", "#FFFFFF"))
				#BGCOL=pygame.Color(labref.attrib.get("BGCOLOR", "#000000"))
				FGCOL=labref.attrib.get("FGCOLOR", "#FFFFFF")
				BGCOL=labref.attrib.get("BGCOLOR", "#000000")
				transp=int(labref.attrib.get("transp", "0"))
				#texfnt=pygame.font.SysFont(None, size)
				pixcnt1=laby
				pixjmp=(size+0)
				textcont=(labref.text + "\n")
				textchunk=""
				#this draws the text body line-per-line
				for texch in textcont:
					if texch=="\n":
						#if at newline, render line of text, clear textchunk, and add to pixcnt1
						#if transp==0:
						#	texgfx=texfnt.render(textchunk, True, FGCOL, BGCOL)
						#else:
						#	texgfx=texfnt.render(textchunk, True, FGCOL)
						texgfx=textrender(textchunk, size, FGCOL, BGCOL, transp)
						screensurf.blit(texgfx, (labx, pixcnt1))
						pixcnt1 += pixjmp
						textchunk=""
					else:
						#if not at a newline yet, keep building textchunk.
						textchunk=(textchunk + texch)
				
				#clickref=screensurf.blit(labgfx, (labx, laby))
		if labref.tag=="label":
			keyid=labref.attrib.get('keyid', "0")
			takekey=labref.attrib.get('takekey', "0")
			onkey=labref.attrib.get('onkey', "0")
			offkey=labref.attrib.get('offkey', "0")
			hoverkey=labref.attrib.get('hoverkey', "0")
			clicksoundflg=int(labref.attrib.get('sfxclick', "0"))
			soundname=(labref.attrib.get('sound', "0"))
			if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
				labx=int(labref.attrib.get("x"))
				laby=int(labref.attrib.get("y"))
				size=int(labref.attrib.get("size"))
				#FGCOL=pygame.Color(labref.attrib.get("FGCOLOR", "#FFFFFF"))
				#BGCOL=pygame.Color(labref.attrib.get("BGCOLOR", "#000000"))
				FGCOL=labref.attrib.get("FGCOLOR", "#FFFFFF")
				BGCOL=labref.attrib.get("BGCOLOR", "#000000")
				labcon=(labref.find("con")).text
				act=labref.find("act")
				acttype=act.attrib.get("type", "none")
				transp=int(labref.attrib.get("transp", "0"))
				#labfnt=pygame.font.SysFont(None, size)
				#if transp==0:
				#	labgfx=labfnt.render(labcon, True, FGCOL, BGCOL)
				#else:
				#	labgfx=labfnt.render(labcon, True, FGCOL)
				labgfx=textrender(labcon, size, FGCOL, BGCOL, transp)
				
				#textrender
				clickref=screensurf.blit(labgfx, (labx, laby))
				if hoverkey!="0":
					if clickref.collidepoint(pos)==1:
						if not hoverkey in keylist:
							keylist.extend([hoverkey])
					else:
						if hoverkey in keylist:
							keylist.remove(hoverkey)
				if acttype!="none":
					pos = pygame.mouse.get_pos()
				if acttype=="iref":
					ref=act.attrib.get("ref")
					datstr=clicktab(clickref, "iref", ref, keyid, takekey, clicksoundflg, soundname)
					clicklist.extend([datstr])
				if acttype=="prev":
					ref=act.attrib.get("ref")
					datstr=clicktab(clickref, "prev", ref, keyid, takekey, clicksoundflg, soundname)
					clicklist.extend([datstr])
				if acttype=="quit":
					ref=act.attrib.get("ref")
					datstr=clicktab(clickref, "quit", ref, keyid, takekey, clicksoundflg, soundname)
					clicklist.extend([datstr])
				if acttype=="key":
					ref=act.attrib.get("ref")
					datstr=clicktab(clickref, "key", ref, keyid, takekey, clicksoundflg, soundname)
					clicklist.extend([datstr])
		#plugin parser
		for pluginst in pluglistactive:
			keyid=labref.attrib.get('keyid', "0")
			takekey=labref.attrib.get('takekey', "0")
			onkey=labref.attrib.get('onkey', "0")
			offkey=labref.attrib.get('offkey', "0")
			clicksoundflg=int(labref.attrib.get('sfxclick', "0"))
			soundname=(labref.attrib.get('sound', "0"))
			hoverkey=labref.attrib.get('hoverkey', "0")
			if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
					
				#textrender
				clickref=pluginst.core(labref)
				if clickref!=None:
					if hoverkey!="0":
						if clickref.collidepoint(pos)==1:
							if not hoverkey in keylist:
								keylist.extend([hoverkey])
						else:
							if hoverkey in keylist:
								keylist.remove(hoverkey)
					act=labref.find("act")
					acttype=act.attrib.get("type", "none")
					if acttype!="none":
						pos = pygame.mouse.get_pos()
					if acttype=="iref":
						ref=act.attrib.get("ref")
						datstr=clicktab(clickref, "iref", ref, keyid, takekey, clicksoundflg, soundname)
						clicklist.extend([datstr])
					if acttype=="prev":
						ref=act.attrib.get("ref")
						datstr=clicktab(clickref, "prev", ref, keyid, takekey, clicksoundflg, soundname)
						clicklist.extend([datstr])
					if acttype=="quit":
						ref=act.attrib.get("ref")
						datstr=clicktab(clickref, "quit", ref, keyid, takekey, clicksoundflg, soundname)
						clicklist.extend([datstr])
					if acttype=="key":
						ref=act.attrib.get("ref")
						datstr=clicktab(clickref, "key", ref, keyid, takekey, clicksoundflg, soundname)
						clicklist.extend([datstr])
	for pluginst in pluglistactive:
		plugret=pluginst.pump()
		if plugret!=None:
			clicklist.extend(plugret)
	
	if qmenuflg==1:
		#qmenudat=(qpopx, qpopy, itemlist, FGCOL, BGCOL, QFNTSIZE)
		menpost=qmenu(qmenudat[0], qmenudat[1], qmenudat[2], fgcol=qmenudat[3], bgcol=qmenudat[4], uipoptextsize=qmenudat[5])
		#qmenu(
		clicklist=(menpost)
	if qpopflg==1:
		poppost=qpop(qpopdat[0], qpopdat[1], qpopdat[2], keyid=(qpopdat[3]), nokey=(qpopdat[4]), quyn=(qpopdat[5]), fgcol=(qpopdat[6]), bgcol=(qpopdat[7]), uipoptextsize=(qpopdat[8]), img=(qpopdat[9]))
		clicklist=(poppost[0])
	if uiquit==1:
		quitxpos=screensurf.get_rect().centerx
		quitypos=screensurf.get_rect().centery
		poppost=qpop(uiquitmsg, quitxpos, quitypos, quyn=1, specialquit=1)
		clicklist=(poppost[0])
	
	if clickfields==1:
		for f in clicklist:
			pygame.draw.rect(screensurf, cfcolor, f.box, 1)
	eventhappen=0
	for event in pygame.event.get():
		#print "nominal"
		eventhappen=1
		if event.type == QUIT:
			uiquit=1
			break
		if event.type == KEYUP:
			if not event.key == K_ESCAPE:
				for pluginst in pluglistactive:
					try:
						pluginst.keyup(event)
					except AttributeError:
						continue
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pausereturn=pause()
				if pausereturn!=None:
					if pausereturn[0]=="quit":
						uiquit=1
						break
					if pausereturn[0]=="load":
						loader(pausereturn[1], 1)
						#reset dialogs
						qmenuflg=0
						qpopflg=0
						break
					if pausereturn[0]=="save":
						saver(pausereturn[1])
						break
					if pausereturn[0]=="newgame":
						qmenuflg=0
						qpopflg=0
						newgame()
						break
			else:
				for pluginst in pluglistactive:
					try:
						pluginst.keydown(event)
					except AttributeError:
						continue
		if event.type==MOUSEBUTTONUP:
			for pluginst in pluglistactive:
				pluginst.clickup(event)
		if event.type==MOUSEBUTTONDOWN:
			for pluginst in pluglistactive:
				pluginst.click(event)
			
			#print "nominal2"
			for f in clicklist:
				#print "nominal3"
				if f.box.collidepoint(event.pos)==1 and event.button==1:
					if f.sfxclick==1:
						clicksound=pygame.mixer.Sound(os.path.join(sfxpath, f.sound))
						clicksound.play()
					if f.keyid!="0":
						if not f.keyid in keylist:
							keylist.extend([f.keyid])
							#print keylist
							keyprint()
					if f.takekey!="0":
						if takekey in keylist and f.takekey!="0":
							keylist.remove(f.takekey)
							#print keylist
							keyprint()
					if f.reftype=="keyx":
						popkey="0"
					if f.reftype=="keym":
						pmenukey="0"
					if f.reftype=="iref":
						vartree.curpage=f.ref
						print(("iref: loading page '" + f.ref + "'"))
						break
					if f.reftype=="prev" and cachepage!="NULL":
						vartree.curpage=cachepage
						print ("prev: go to previous page")
						break
					if f.reftype=="quit":
						uiquit=1
						break
					if f.reftype=="report":
						try:
							f.ref.clickreport(f)
						except AttributeError:
							print("Error: report reftype missing refrence to plugin instance,\n or plugin instance missing clickreport method.")
					if f.reftype=="quitx":
						print ("quit: onclick quit")
						quitflag=1
						break
					if f.quitab==1:
						uiquit=0
					if f.quitab==2:
						qpopflg=0
					if f.quitab==3:
						qmenuflg=0
	#if eventhappen==0:
	#	time.sleep(0.01)

		
	pygame.display.flip()
	pygame.event.pump()

saver()
print("Done.")