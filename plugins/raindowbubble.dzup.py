#!/usr/bin/env python

class PLUGIN_rainbowbubbles:
	def __init__(self, screensurf, keylist, vartree):
		self.screensurf=screensurf
		self.keylist=keylist
		self.cloudlist=[]
		self.defxpos=-60
		self.cloudspec=pygame.Surface((2, 2))
		self.cloudspec.fill((255, 255, 255))
		self.cloudspec2=pygame.Surface((3, 3))
		self.cloudspec2.fill((255, 255, 255))
		self.cloudspec3=pygame.Surface((4, 4))
		self.cloudspec3.fill((255, 255, 255))
		self.xlimit=screensurf.get_width()+45
		self.ylimit=screensurf.get_height()+45
		self.cloudcolor=pygame.Color(255, 255, 255)
		self.cloudon=0
		self.cloudreflow=1
	def fork(self, tagobj):
		if tagobj.tag=="rainbowbubblereset":
			self.resetkeyid=tagobj.attrib.get("keyid")
			if self.resetkeyid in self.keylist:
				self.cloudreflow=0
				self.cloudlist=[]
				self.keylist.remove(self.resetkeyid)
	def core(self, tagobj):
		if tagobj.tag=="rainbowbubble":
			self.cloudon=1
			self.cloudreflow=0
			for self.clouddot in self.cloudlist:
				#self.screensurf.blit(self.cloudpoint, (self.clouddot[0], self.clouddot[1]))
				if self.clouddot[4]<=2:
					cwidth=0
				else:
					cwidth=1
				pygame.draw.circle(self.screensurf, self.clouddot[3], (self.clouddot[0], int(self.clouddot[1])), self.clouddot[2]*5, cwidth)
				
	def pump(self):
		#flow loop zero times per pump if nothing happening
		self.flowloop=[]
		#normal flow loop per pump count:
		if self.cloudon==1:
			self.flowloop=[1]
		#loop per pump for background reflow:
		if self.cloudreflow==1:
			#print "reflow"
			self.flowloop=[1, 2, 3, 4, 5]
		#flow loop
		for self.d in self.flowloop:
			#cloudflake creation
			#add slight bias for slower cloud
			for self.f in [1]:
				colorbit=random.randint(200, 255)
				colorpair=(colorbit, colorbit, colorbit)
				self.cloudlist.extend([[self.defxpos, random.randint(0, self.ylimit), random.randint(4, 7), colorpair, random.randint(0, 3), random.uniform(-1, 1)]])
			#normal cloud function
			for self.f in [1]:
				colorbit=random.randint(200, 255)
				colorpair=(random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
				self.cloudlist.extend([[self.defxpos, random.randint(0, self.ylimit), random.randint(4, 10), colorpair, random.randint(0, 3), random.uniform(-1, 1)]])
			#cloudflake position incrementer (notice how the speed is determined by the third item in the cloudflake's lists
			for self.clouddot in self.cloudlist:
				self.clouddot[0] += self.clouddot[2]
				#remove cloudflakes once they are below the botton of the screen.
				if self.clouddot[0]>self.xlimit:
					self.cloudlist.remove(self.clouddot)
					if self.clouddot[2]==4:
						self.cloudreflow=0
				elif self.clouddot[1]>self.ylimit:
					self.clouddot[1]=-44
				elif self.clouddot[1]<-45:
					self.clouddot[1]=self.ylimit-1
				self.clouddot[1]+=self.clouddot[5]
			#turn off cloud active flag, (if a cloudfx tag is present and active in core, it will reenable it.)
			#this lets onkey/offkey masking pause the cloud processing when no cloudfx tag is active and present.
			self.cloudon=0
			#print len(self.cloudlist)
			if self.cloudreflow==0:
				break
			
		return
	def click(self, event):
		return
	def clickup(self, event):
		return
	def pageclear(self):
		self.cloudon=0
		self.cloudreflow=1
		return


#using this plugin is easy. just place the core tag: <rainbowbubble/> in the location in core you want.
#also note that its best to use only ONE rainbowbubble tag, as using two will waste cpu as it will render the same thing.

#by default cloudfx will try to keep a full screen of bubbles ready.
#if you want the cloud to start falling "magically" trigger the keyid fork tag, <rainbowbubblereset keyid="triggeringkey"/>
#the keyid is removed when triggered.

#its recommended to trigger this when the page loads. that way when first render happens, it will be reset.

#rainbow bubble plugin for Desutezeoid
#by Thomas Leathers
plugname="Rainbow Bubbles"
plugclass=PLUGIN_rainbowbubbles
plugpath="raindowbubble.dzup"