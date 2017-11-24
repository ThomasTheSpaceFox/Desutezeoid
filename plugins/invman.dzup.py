#!/usr/bin/env python

class PLUGIN_invman:
	def __init__(self, screensurf, keylist, vartree):
		self.vartree=vartree
		self.screensurf=screensurf
		self.keylist=keylist
		self.playitems=[]
		self.knownids=[]
		self.huditemsize=40
		self.huditemjmp=42
		self.hudheight=48
		self.rectlist=[]
		self.selitem=None
		self.resetselitem=0
	def fork(self, tagobj):
		#item give fork
		if tagobj.tag=="giveitem":
			self.keyid=tagobj.attrib.get("keyid")
			
			if self.keyid in self.keylist:
				self.keylist.remove(self.keyid)
				self.itemid=tagobj.attrib.get("itemid")
				self.itemname=tagobj.attrib.get("name")
				self.postkey=tagobj.attrib.get("postkey", "0")
				self.iconname=tagobj.attrib.get("icon")
				print self.iconname
				if self.itemid not in self.knownids:
					if self.postkey not in self.keylist:
						self.keylist.extend([self.postkey])
					self.icongfx=pygame.image.load(os.path.join("img", self.iconname)).convert_alpha()
					#add itemid to knownids
					self.knownids.extend([self.itemid])
					#item creation
					self.playitems.extend([[self.itemid, self.itemname, self.icongfx, self.iconname]])
		#item take fork
		if tagobj.tag=="takeitem":
			
			self.keyid=tagobj.attrib.get("keyid")
			if self.keyid in self.keylist:
				self.keylist.remove(self.keyid)
				self.itemid=tagobj.attrib.get("itemid")
				self.postkey=tagobj.attrib.get("postkey", "0")
				if self.itemid in self.knownids:
					if self.postkey not in self.keylist:
						self.keylist.extend([self.postkey])
					#remove itemid from knownids
					self.knownids.remove(self.itemid)
					#find and remove the item from playitems
					for self.itemx in self.playitems:
						if self.itemx[0]==self.itemid:
							self.playitems.remove(self.itemx)
							break
		return
	def core(self, tagobj):
		#action rectangle core object
		if tagobj.tag=="actionrect":
			self.keyid=tagobj.attrib.get("keyid")
			self.cx=int(tagobj.attrib.get("x"))
			self.cy=int(tagobj.attrib.get("y"))
			self.csx=int(tagobj.attrib.get("sizex"))
			self.csy=int(tagobj.attrib.get("sizey"))
			self.itemid=tagobj.attrib.get("itemid")
			self.rectlist.extend([dzulib.ctreport(pygame.Rect(self.cx, self.cy, self.csx, self.csy), self, ["act", self.itemid, self.keyid])])
		#item hud core object. (only one of these should be used per page!)
		if tagobj.tag=="itemhud":
			self.cx=int(tagobj.attrib.get("x"))
			self.cy=int(tagobj.attrib.get("y"))
			FGCOL=dzulib.colorify(tagobj.attrib.get("FGCOLOR", self.vartree.uifgcolorstr))
			BGCOL=dzulib.colorify(tagobj.attrib.get("BGCOLOR", self.vartree.uibgcolorstr))
			#self.itemlimit=int(tagobj.attrib.get("itemlimit", "8"))
			self.itemlimit=len(self.playitems)
			self.hudrect=pygame.Rect(self.cx, self.cy, (self.itemlimit*self.huditemjmp)+6, self.hudheight)
			pygame.draw.rect(self.screensurf, BGCOL, self.hudrect, 0)
			#pygame.draw.rect(self.screensurf, (255, 255, 255), self.hudrect, 1)
			dzulib.trace3dbox(self.screensurf, BGCOL, self.hudrect, 2)
			self.iposy=self.cy+4
			self.iposx=self.cx+4
			for self.itemx in self.playitems:
				self.itemrect=self.screensurf.blit(self.itemx[2], (self.iposx, self.iposy))
				pygame.draw.rect(self.screensurf, FGCOL, self.itemrect, 1)
				self.rectlist.extend([dzulib.ctreport(self.itemrect, self, ["hud", self.itemx])])
				self.iposx += self.huditemjmp
				
			
		return
	def pump(self):
		#selected item "float" code
		if self.selitem!=None:
			self.mpos=pygame.mouse.get_pos()
			self.screensurf.blit(self.selitem[2], (self.mpos[0], self.mpos[1]))
			#reset selected item if resetselitem is set to one by click method
			if self.resetselitem==1:
				self.resetselitem=0
				self.selitem=None
		self.returnlist=self.rectlist
		self.rectlist=[]
		return self.returnlist
	def click(self, event):
		#the selected item is not reset here in order for the action portion of clickreport to work right...
		if self.selitem!=None:
			#self.selitem=None
			self.resetselitem=1
	def clickup(self, event):
		return
	def pageclear(self):
		return
	def clickreport(self, clickinst):
		self.datarep=clickinst.data
		if self.datarep[0]=="act":
			if self.selitem!=None:
				#print "selact"
				if self.datarep[1] == self.selitem[0]:
					if self.datarep[2] not in self.keylist:
						self.keylist.extend([self.datarep[2]])
		if self.datarep[0]=="hud":
			self.selitem=self.datarep[1]
	def cnfload(self, plugcnf):
		return
	def savload(self, savtag):
		for self.savitem in savtag.findall("invitem"):
			self.itemid=self.savitem.attrib.get("itemid")
			self.itemname=self.savitem.attrib.get("itemname")
			self.iconname=self.savitem.attrib.get("iconname")
			#print self.itemname
			self.icongfx=pygame.image.load(os.path.join("img", self.iconname)).convert_alpha()
			self.knownids.extend([self.itemid])
			#item creation
			self.playitems.extend([[self.itemid, self.itemname, self.icongfx, self.iconname]])
	def savwrite(self, savtag):
		for self.savitem in savtag.findall("invitem"):
			savtag.remove(self.savitem)
		for self.savitem in self.playitems:
			self.savelem=ET.SubElement(savtag, 'invitem')
			self.savelem.set("itemid", str(self.savitem[0]))
			self.savelem.set("itemname", str(self.savitem[1]))
			self.savelem.set("iconname", str(self.savitem[3]))
			#print self.savitem[1]
		return



plugname="Inventory Manager Plugin"
plugclass=PLUGIN_invman
plugpath=None