#!/usr/bin/env python

class PLUGIN_shaders_tonefx:
	def __init__(self, screensurf, keylist, vartree):
		self.screensurf=screensurf
		self.keylist=keylist
		#best practice to init keyid variables during init, and default them to "0" (the null keyid)
		self.keyid="0"
		self.fxh=screensurf.get_height()
		self.fxw=screensurf.get_width()
		self.fxsurf=pygame.Surface((self.fxw, self.fxh)).convert(screensurf)
		self.fxsurf.fill((60, 60, 60))
		self.fxsurf2=pygame.Surface((self.fxw, self.fxh)).convert(screensurf)
		self.fxsurf2.fill((30, 30, 30))
	def fork(self, tagobj):
		
		return
	def core(self, tagobj):
		if tagobj.tag=="shadcolorfade":
			self.screensurf.blit(self.fxsurf, (0, 0), special_flags = pygame.BLEND_SUB)
			self.screensurf.blit(self.fxsurf, (0, 0), special_flags = pygame.BLEND_ADD)
		if tagobj.tag=="shadvalueboost":
			self.screensurf.blit(self.fxsurf2, (0, 0), special_flags = pygame.BLEND_ADD)
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



#color tone shader





plugname="shaders - tonefx"
plugclass=PLUGIN_shaders_tonefx
plugpath=None