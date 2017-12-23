#!/usr/bin/env python

class PLUGIN_rainfx:
	def __init__(self, screensurf, keylist, vartree):
		self.screensurf=screensurf
		self.keylist=keylist
		self.rainlist=[]
		self.defypos=-50
		self.rainxoff=0
		self.rainyoff=20
		self.rainyoff2=35
		self.rainyoff3=50
		self.rainvector=0
		self.xlimit=screensurf.get_width() - 1
		self.ylimit=screensurf.get_height() - 1
		self.raincolor=pygame.Color(200, 200, 200)
		self.raincolor2=pygame.Color(190, 190, 190)
		self.raincolor3=pygame.Color(180, 180, 180)
		self.rainon=0
		self.rainreflow=1
	def fork(self, tagobj):
		if tagobj.tag=="rainreset":
			self.resetkeyid=tagobj.attrib.get("keyid")
			if self.resetkeyid in self.keylist:
				self.rainvector=int(tagobj.attrib.get("vector", str(self.rainvector)))
				self.rainreflow=0
				self.rainlist=[]
				self.keylist.remove(self.resetkeyid)
	def core(self, tagobj):
		if tagobj.tag=="rainfx":
			self.rainon=1
			self.rainreflow=0
			for self.raindot in self.rainlist:
				if self.raindot[2]>50:	
					pygame.draw.line(self.screensurf, self.raincolor, (self.raindot[0], self.raindot[1]), ((self.raindot[0] - (self.raindot[3]*2)), (self.raindot[1] - self.rainyoff3)), 1)
				elif self.raindot[2]>40:	
					pygame.draw.line(self.screensurf, self.raincolor2, (self.raindot[0], self.raindot[1]), ((self.raindot[0] - (self.raindot[3])), (self.raindot[1] - self.rainyoff2)))
				else:
					pygame.draw.line(self.screensurf, self.raincolor3, (self.raindot[0], self.raindot[1]), ((self.raindot[0] - (self.raindot[3]//2)), (self.raindot[1] - self.rainyoff)))
				
	def pump(self):
		#flow loop zero times per pump if nothing happening
		self.flowloop=[]
		#normal flow loop per pump count:
		if self.rainon==1:
			self.flowloop=[1]
		#loop per pump for background reflow:
		if self.rainreflow==1:
			#print "reflow"
			self.flowloop=[1, 2, 3, 4, 5]
		#flow loop
		for self.d in self.flowloop:
			#rain particle creation
			#add slight bias for slower rain
			for self.f in [1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3]:
				self.rainlist.extend([[random.randint(0, self.xlimit), self.defypos, random.randint(30, 40), random.randint(self.rainvector - 2, self.rainvector + 2)]])
			#normal rain function
			for self.f in [1, 2, 3, 4, 5, 6, 7, 8]:
				self.rainlist.extend([[random.randint(0, self.xlimit), self.defypos, random.randint(30, 60), random.randint(self.rainvector - 2, self.rainvector + 2)]])
			#rain particle position incrementer (notice how the speed is determined by the third item in the rain particle's lists
			for self.raindot in self.rainlist:
				self.raindot[1] += self.raindot[2]
				self.raindot[0] += self.raindot[3]
				if self.raindot[0]>self.xlimit:
					self.raindot[0] -= self.xlimit+10
				elif self.raindot[0]<-10:
					self.raindot[0] += self.xlimit
				#remove rain particles once they are below the botton of the screen.
				if self.raindot[1] - self.rainyoff>self.ylimit:
					self.rainlist.remove(self.raindot)
					if self.raindot[2]==30:
						self.rainreflow=0
			#turn off rain active flag, (if a rainfx tag is present and active in core, it will reenable it.)
			#this lets onkey/offkey masking pause the rain processing when no rainfx tag is active and present.
			self.rainon=0
			#print len(self.rainlist)
			if self.rainreflow==0:
				break
			
		return
	def click(self, event):
		return
	def clickup(self, event):
		return
	def pageclear(self):
		self.rainon=0
		self.rainreflow=1
		return


#using this plugin is easy. just place the core tag: <rainfx/> in the location in core you want.
#also note that its best to use only ONE rainfx tag, as using two will waste cpu as it will render the same thing.

#by default rainfx will try to keep a full screen of rain particles ready.
#if you want the rain to start falling "magically" trigger the keyid fork tag, <rainreset keyid="triggeringkey"/>
#the keyid is removed when triggered.

#its recommended to trigger this when the page loads. that way when first render happens, it will be reset.

#RainFX plugin for Desutezeoid
#Based upon SnowFX
#by Thomas Leathers
plugname="RainFX"
plugclass=PLUGIN_rainfx
plugpath=None