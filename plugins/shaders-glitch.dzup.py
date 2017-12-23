#!/usr/bin/env python

class PLUGIN_shaders_glitch:
	def __init__(self, screensurf, keylist, vartree):
		self.screensurf=screensurf
		self.keylist=keylist
		#best practice to init keyid variables during init, and default them to "0" (the null keyid)
		self.keyid="0"
		self.glitchy=0
		self.glitchlimit=self.screensurf.get_height()+30
		self.glitchrollover=self.screensurf.get_height()+2000
		
		self.glitchhig=30
		self.glitchwid=self.screensurf.get_width()-1
	def fork(self, tagobj):
		
		return
	def core(self, tagobj):
		if tagobj.tag=="shadglitch1":
			if  self.glitchy<self.glitchlimit:
				self.screensurf.set_clip(pygame.Rect(0, self.glitchy, self.glitchwid, self.glitchhig))
				self.screensurf.scroll(20, 0)
				self.screensurf.set_clip(None)
			self.glitchy += 20
			if self.glitchy>self.glitchrollover:
				self.glitchy=0
		return
	def pump(self):
		return
	#called on pygame mousebuttondown events
	def click(self, event):
		return
	#called on pygame mousebuttonup events
	def clickup(self, event):
		return
	#called upon page load.
	def pageclear(self):
		return





#Screen glitch shader plugin.



plugname="shaders - glitch"
plugclass=PLUGIN_shaders_glitch
plugpath=None