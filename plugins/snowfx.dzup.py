#!/usr/bin/env python

class PLUGIN_snowfx:
	def __init__(self, screensurf, keylist, vartree):
		self.screensurf=screensurf
		self.keylist=keylist
		self.snowlist=[]
		self.defypos=0
		self.snowspec=pygame.Surface((2, 2)).convert(self.screensurf)
		self.snowspec.fill((255, 255, 255))
		self.snowspec2=pygame.Surface((3, 3)).convert(self.screensurf)
		self.snowspec2.fill((255, 255, 255))
		self.snowspec3=pygame.Surface((4, 4)).convert(self.screensurf)
		self.snowspec3.fill((255, 255, 255))
		self.xlimit=screensurf.get_width() - 1
		self.ylimit=screensurf.get_height() - 1
		self.snowcolor=pygame.Color(255, 255, 255)
		self.snowon=0
		self.snowreflow=1
	def fork(self, tagobj):
		if tagobj.tag=="snowreset":
			self.resetkeyid=tagobj.attrib.get("keyid")
			if self.resetkeyid in self.keylist:
				self.snowreflow=0
				self.snowlist=[]
				self.keylist.remove(self.resetkeyid)
	def core(self, tagobj):
		if tagobj.tag=="snowfx":
			self.snowon=1
			self.snowreflow=0
			for self.snowdot in self.snowlist:
				#self.fxpix[self.snowdot[0], self.snowdot[1]] = self.snowcolor
				#for faster snowflakes use slightly larger snow, else, use smaller.
				if self.snowdot[2]>9:
					self.screensurf.blit(self.snowspec3, (self.snowdot[0], self.snowdot[1]))
				elif self.snowdot[2]>7:
					self.screensurf.blit(self.snowspec2, (self.snowdot[0], self.snowdot[1]))
				else:
					self.screensurf.blit(self.snowspec, (self.snowdot[0], self.snowdot[1]))
				
	def pump(self):
		#flow loop zero times per pump if nothing happening
		self.flowloop=[]
		#normal flow loop per pump count:
		if self.snowon==1:
			self.flowloop=[1]
		#loop per pump for background reflow:
		if self.snowreflow==1:
			#print "reflow"
			self.flowloop=[1, 2, 3, 4, 5]
		#flow loop
		for self.d in self.flowloop:
			#snowflake creation
			#add slight bias for slower snow
			for self.f in [1, 2]:
				self.snowlist.extend([[random.randint(0, self.xlimit), self.defypos, random.randint(4, 7)]])
			#normal snow function
			for self.f in [1, 2, 3, 4, 5]:
				self.snowlist.extend([[random.randint(0, self.xlimit), self.defypos, random.randint(4, 10)]])
			#snowflake position incrementer (notice how the speed is determined by the third item in the snowflake's lists
			for self.snowdot in self.snowlist:
				self.snowdot[1] += self.snowdot[2]
				#remove snowflakes once they are below the botton of the screen.
				if self.snowdot[1]>self.ylimit:
					self.snowlist.remove(self.snowdot)
					if self.snowdot[2]==4:
						self.snowreflow=0
			#turn off snow active flag, (if a snowfx tag is present and active in core, it will reenable it.)
			#this lets onkey/offkey masking pause the snow processing when no snowfx tag is active and present.
			self.snowon=0
			#print len(self.snowlist)
			if self.snowreflow==0:
				break
			
		return
	def click(self, event):
		return
	def clickup(self, event):
		return
	def pageclear(self):
		self.snowon=0
		self.snowreflow=1
		return


#using this plugin is easy. just place the core tag: <snowfx/> in the location in core you want.
#also note that its best to use only ONE snowfx tag, as using two will waste cpu as it will render the same thing.

#by default snowfx will try to keep a full screen of snowflakes ready.
#if you want the snow to start falling "magically" trigger the keyid fork tag, <snowreset keyid="triggeringkey"/>
#the keyid is removed when triggered.

#its recommended to trigger this when the page loads. that way when first render happens, it will be reset.

#snowfx plugin for Desutezeoid
#by Thomas Leathers
plugname="SnowFX"
plugclass=PLUGIN_snowfx
plugpath=None