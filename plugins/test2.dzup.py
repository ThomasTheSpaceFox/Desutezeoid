#!/usr/bin/env python

class PLUGIN_test_test2:
	def __init__(self, screensurf, keylist):
		self.screensurf=screensurf
		self.keylist=keylist
		#best practice to init keyid variables during init, and default them to "0" (the null keyid)
		self.keyid="0"
	def fork(self, tagobj):
		return
	#core object. should either return None, or pygame Rect.
	#if Rect is returned, the system will attempt to parse the standard
	#"act" component, and associated related attributes...
	#you may also want to use the provided click events in place of the standard act component.
	#if you want hoverkey to be active, you MUST return a Rect!
	#onkey/offkey masking is honored by the system regardless.
	def core(self, tagobj):
		if tagobj.tag=="test2":
			xpos=int(tagobj.attrib.get("x"))
			ypos=int(tagobj.attrib.get("y"))
			self.testrect=pygame.Rect(xpos, ypos, 60, 20)
			pygame.draw.rect(self.screensurf, (0, 127, 255), self.testrect)
			return self.testrect
	#called every loop. 
	def pump(self):
		return
	#called on pygame mousebuttondown events
	def click(self, event):
		return
	#called on pygame mousebuttonup events
	def clickup(self, event):
		return
	#called upon page load
	def pageclear(self):
		return









plugname="test plugin2"
plugclass=PLUGIN_test_test2
plugpath="test.dzup"