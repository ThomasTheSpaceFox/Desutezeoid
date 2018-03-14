#!/usr/bin/env python

class PLUGIN_dza_dza:
	def __init__(self, screensurf, keylist, vartree):
		self.screensurf=screensurf
		self.keylist=keylist
		#best practice to init keyid variables during init, and default them to "0" (the null keyid)
		self.keyid="0"
		self.animlist=[]
		self.loadflag=0
	def fork(self, tagobj):
		if tagobj.tag=="anim":
			self.keyid=tagobj.attrib.get("keyid", "0")
			self.globflg=int(tagobj.attrib.get("global", "0"))
			self.layer=int(tagobj.attrib.get("layer", "0"))
			self.stopkey=tagobj.attrib.get("stopkey", "0")
			if self.keyid in self.keylist and self.keyid!="0":
				self.keylist.remove(self.keyid)
				self.anim=tagobj.attrib.get("anim")
				try:
					self.animfile=open(os.path.join("anim", self.anim), "r")
				except IOError:
					print("WARNING: Failed to load DZA script: \"" + self.anim + "\"")
					return
				self.animlist.extend([[self._animload_(self.animfile), 0, None, None, 0, 0, self.stopkey, self.anim, "none", self.globflg, self.layer]])
		
		return
	def core(self, tagobj):
		if tagobj.tag=="animsurf":
			self.layer=int(tagobj.attrib.get("layer", "0"))
			for anim in self.animlist:
				animsurf=anim[3]
				if animsurf!=None and anim[10]==self.layer:
					self.screensurf.blit(animsurf, (anim[4], anim[5]))
		return
	def pump(self):
		#DZA script parser core
		for anim in self.animlist:
			#print(anim)
			framepassed=0
			#loop until any non-frame function lines are parsed.
			while framepassed==0:
				animset=anim[0]
				#stopkey check
				if anim[6] in self.keylist and anim[6]!="0":
					self.animlist.remove(anim)
					self.keylist.remove(anim[6])
					#print("script exit stopkey")
					framepassed=1
					break
				else:
					
					if anim[1]<0:
						print("amim: pointer underflow")
						anim[1]=0
					if anim[2]==None:
						anim[2]=0
						skipparse=0
					elif anim[2]==0:
						anim[1]+=1
						skipparse=0
					
					else:
						anim[2]-=1
						skipparse=1
					#DZA-script function parser
					if not skipparse:
						#print(anim[1])
						animblock=animset[anim[1]]
						animcmd=animblock[0]
						if animcmd=="x":
							self.animlist.remove(anim)
							framepassed=1
							#print("script exit x")
							break
						#add keyid
						if animcmd=="k":
							kkey=animblock[1]
							if kkey not in self.keylist:
								self.keylist.extend([kkey])
						#remove keyid
						if animcmd=="r":
							kkey=animblock[1]
							if kkey in self.keylist and kkey!="0":
								self.keylist.remove(kkey)
						#sound
						if animcmd=="s":
							try:
								sound=animblock[1]
								if sound!=None:
									sound.play()
							except pygame.error:
								continue
						#unconditional goto
						if animcmd=="g":
							goloopstr=animblock[2]
							if goloopstr=="i":
								anim[1]=int(animblock[1])-1
								anim[2]=None
							else:
								goloop=int(goloopstr)
								if goloop>0:
									anim[1]=int(animblock[1])-1
									anim[2]=None
									if goloop==-1:
										animblock[2]=goloop-1
						#conditional goto
						if animcmd=="cg":
							congokey=animblock[3]
							if congokey in self.keylist:
								goloopstr=animblock[2]
								if goloopstr=="i":
									anim[1]=int(animblock[1])-1
									anim[2]=None
								else:
									goloop=int(goloopstr)
									if goloop>0:
										anim[1]=int(animblock[1])-1
										anim[2]=None
										if goloop==-1:
											animblock[2]=goloop-1
						#the wait and frame commands are the only commands that trigger framepassed.
						#this and the acompanying while loop cause non-frame commands to be parsed quickly "between frames"
						if animcmd=="w":
							anim[2]=int(animblock[1])
							anim[3]=None
							anim[8]="none"
							framepassed=1
						if animcmd=="f":
							anim[8]=animblock[1]
							anim[3]=dzulib.filelookup(animblock[1])
							anim[2]=int(animblock[2])
							anim[4]=int(animblock[3])
							anim[5]=int(animblock[4])
							framepassed=1
					else:
						framepassed=1
	def click(self, event):
		return
	def clickup(self, event):
		return
	def pageclear(self):
		#ignore pageclear if a save-state was just loaded
		if self.loadflag==1:
			self.loadflag=0
		else:
			#terminate non-global DZA script instances.
			for anim in self.animlist:
				if anim[9]==0:
					self.animlist.remove(anim)
		return
	def cnfload(self, plugcnf):
		return
	def _animload_(self, animfile):
		animset=list()
		for line in animfile.readlines():
			#remove newline chars and ignore comments.
			linex=((line.replace("\n", "")).split("#"))[0]
			if not linex=="":
				linelist=linex.split(";")
				#preload samples and cache them into list structure.
				if linelist[0]=="s":
					try:
						linelist[1]=pygame.mixer.Sound(os.path.join("sfx", linelist[1]))
					except pygame.error:
						linelist[1]=None
						
				animset.extend([linelist])
		#add exit at end of script.
		animset.extend([["x"]])
		#print(animset)
		return animset
	def savload(self, savtag):
		self.animlist=[]
		self.loadflag=1
		for self.savitem in savtag.findall("DZAscriptpointer"):
			#print("barfoo")
			try:
				framecountdown=self.savitem.attrib.get("framecountdown")
				point=int(self.savitem.attrib.get("point"))
				x=int(self.savitem.attrib.get("x"))
				layer=int(self.savitem.attrib.get("layer"))
				self.globflg=int(self.savitem.attrib.get("global"))
				y=int(self.savitem.attrib.get("y"))
				#parse vars that might not be ints.
				if framecountdown=="none":
					framecountdown=None
				else:
					framecountdown=int(framecountdown)
				if self.savitem.attrib.get("image")=="none":
					image=None
				else:
					image=dzulib.filelookup(self.savitem.attrib.get("image"))
				stopkey=(self.savitem.attrib.get("stopkey"))
				anim=(self.savitem.attrib.get("anim"))
				self.animlist.extend([[self._animload_(open(os.path.join("anim", anim), "r")), point, framecountdown, image, x, y, stopkey, anim, "none", self.globflg, layer]])
			except AttributeError as e:
				print(e)
				print("fault")
			#print(self.animlist)
	def savwrite(self, savtag):
		#remove old script pointers
		for self.savitem in savtag.findall("DZAscriptpointer"):
			savtag.remove(self.savitem)
		#save each active script and its variout params as an element.
		for self.scriptitem in self.animlist:
			self.scriptelem=ET.SubElement(savtag, 'DZAscriptpointer')
			self.scriptelem.set("point", str(self.scriptitem[1]))
			self.scriptelem.set("framecountdown", str(self.scriptitem[2]))
			self.scriptelem.set("x", str(self.scriptitem[4]))
			self.scriptelem.set("y", str(self.scriptitem[5]))
			self.scriptelem.set("stopkey", str(self.scriptitem[6]))
			self.scriptelem.set("anim", str(self.scriptitem[7]))
			self.scriptelem.set("image", str(self.scriptitem[8]))
			self.scriptelem.set("global", str(self.scriptitem[9]))
			self.scriptelem.set("layer", str(self.scriptitem[10]))



#this plugin provides Desutezeoid with a script-based sequencing and animation system.
#scripts can be rendered on as many layers as needed.
#for example: you could have one animation behind a window, and another in front of it.





plugname="DZA: Desutezeoid Animation system."
plugclass=PLUGIN_dza_dza
plugpath=None