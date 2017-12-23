#!/usr/bin/env python

class PLUGIN_shaders_crtmon:
	def __init__(self, screensurf, keylist, vartree):
		self.screensurf=screensurf
		self.keylist=keylist
		#best practice to init keyid variables during init, and default them to "0" (the null keyid)
		self.keyid="0"
		self.fxh=screensurf.get_height()
		self.fxw=screensurf.get_width()
		self.fxsurf=pygame.Surface((self.fxw, self.fxh)).convert(screensurf)
		self.fxsurf.fill((255, 0, 255))
		self.fxsurf2=pygame.Surface((self.fxw, self.fxh)).convert(screensurf)
		self.fxsurf2.fill((0, 0, 0))
		self.hlinejump=4
		self.hline=0
		while self.hline<=self.fxw:
			pygame.draw.line(self.fxsurf, (255, 70, 255), (self.hline, 0), (self.hline, self.fxh), 2)
			self.hline += self.hlinejump
		self.hline=0
		while self.hline<=self.fxw:
			pygame.draw.line(self.fxsurf2, (70, 70, 70), (self.hline, 0), (self.hline, self.fxh), 2)
			self.hline += self.hlinejump
	def fork(self, tagobj):
		
		return
	def core(self, tagobj):
		if tagobj.tag=="shadcrtgreen":
			self.screensurf.blit(self.fxsurf, (0, 0), special_flags = pygame.BLEND_SUB)
		if tagobj.tag=="shadcrtcolor":
			self.screensurf.blit(self.fxsurf2, (0, 0), special_flags = pygame.BLEND_SUB)
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



#crt monitor scanline shader
#uses shadcrtgreen for a green effect
#use shadcrtcolor for a color effect





plugname="shaders - crtmon"
plugclass=PLUGIN_shaders_crtmon
plugpath=None