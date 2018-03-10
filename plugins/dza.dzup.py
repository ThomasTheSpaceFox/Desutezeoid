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
			self.stopkey=tagobj.attrib.get("stopkey", "0")
			if self.keyid in self.keylist and self.keyid!="0":
				self.keylist.remove(self.keyid)
				self.anim=tagobj.attrib.get("anim")
				try:
					self.animfile=open(os.path.join("anim", self.anim), "r")
				except IOError:
					return
				self.animlist.extend([[self._animload_(self.animfile), 0, None, None, 0, 0, self.stopkey, self.anim, "none", self.globflg]])
		
		return
	def core(self, tagobj):
		return
	def pump(self):
		
		for anim in self.animlist:
			#print(anim)
			framepassed=0
			#loop until any non-frame function lines are parsed.
			while framepassed==0:
				animset=anim[0]
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
						if animcmd=="s":
							try:
								sound=animblock[1]
								if sound!=None:
									sound.play()
							except pygame.error:
								continue
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
						if animcmd=="w":
							anim[2]=int(animblock[1])
							anim[3]=None
							anim[8]="none"
						if animcmd=="f":
							anim[8]=animblock[1]
							anim[3]=dzulib.filelookup(animblock[1])
							anim[2]=int(animblock[2])
							anim[4]=int(animblock[3])
							anim[5]=int(animblock[4])
							framepassed=1
					else:
						framepassed=1
					animsurf=anim[3]
					if animsurf!=None:
						self.screensurf.blit(animsurf, (anim[4], anim[5]))
	#called on pygame mousebuttondown events
	def click(self, event):
		return
	#called on pygame mousebuttonup events
	def clickup(self, event):
		return
	#called upon page load.
	def pageclear(self):
		if self.loadflag==1:
			self.loadflag=0
		else:
			for anim in self.animlist:
				if anim[9]==0:
					self.animlist.remove(anim)
		return
	#optional config load tag. queries all plugins with each tag in the plugcnf section
	def cnfload(self, plugcnf):
		return
	def _animload_(self, animfile):
		animset=list()
		for line in animfile.readlines():
			linex=((line.replace("\n", "")).split("#"))[0]
			if not linex=="":
				linelist=linex.split(";")
				#preload samples
				if linelist[0]=="s":
					try:
						linelist[1]=pygame.mixer.Sound(os.path.join("sfx", linelist[1]))
					except pygame.error:
						linelist[1]=None
						
				animset.extend([linelist])
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
				self.globflg=int(self.savitem.attrib.get("global"))
				y=int(self.savitem.attrib.get("y"))
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
				self.animlist.extend([[self._animload_(open(os.path.join("anim", anim), "r")), point, framecountdown, image, x, y, stopkey, anim, "none", self.globflg]])
			except AttributeError as e:
				print(e)
				print("fault")
			#print(self.animlist)
	def savwrite(self, savtag):
		for self.savitem in savtag.findall("DZAscriptpointer"):
			savtag.remove(self.savitem)
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









plugname="DZA: Desutezeoid Animation system."
plugclass=PLUGIN_dza_dza
plugpath=None