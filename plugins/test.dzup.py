#!/usr/bin/env python

class PLUGIN_test_test:
	def __init__(self, screensurf, keylist):
		self.screensurf=screensurf
		self.keylist=keylist
		#best practice to init keyid variables during init, and default them to "0" (the null keyid)
		self.keyid="0"
	def fork(self, tagobj):
		if tagobj.tag=="testfork":
			self.keyid=tagobj.attrib.get("keyid", "0")
		
		return
	#core object. should either return None, or pygame Rect.
	#if Rect is returned, the system will attempt to parse the standard
	#"act" component, and associated related attributes...
	#you may also want to use the provided click events in place of the standard act component.
	#if you want hoverkey to be active, you MUST return a Rect!
	#onkey/offkey masking is honored by the system regardless.
	def core(self, tagobj):
		if tagobj.tag=="test":
			self.xpos=int(tagobj.attrib.get("x"))
			self.ypos=int(tagobj.attrib.get("y"))
			#flag controlling the below pump example.
			self.coreprocessed=1
			self.testrect=pygame.Rect(self.xpos, self.ypos, 60, 60)
			if self.keyid in self.keylist:
				pygame.draw.rect(self.screensurf, (0, 0, 0), self.testrect)
			else:
				pygame.draw.rect(self.screensurf, (255, 255, 255), self.testrect)
		return
	#called every loop. Return a list of dzulib.clicktab instances
	#to have them appended to the clicklist.
	#this example builds a clicktab of the most recent "test" core tag processed.
	def pump(self):
		if self.coreprocessed==1:
			#arguments explained in order: pygame Rect, refrence type, refrence, keyid, takekey, sfxclick flag, sound. 
			return [dzulib.clicktab(self.testrect, "key", None, "testpumpappend", "0", "0", None)]
	#called on pygame mousebuttondown events
	def click(self, event):
		return
	#called on pygame mousebuttonup events
	def clickup(self, event):
		return
	#called upon page load.
	def pageclear(self):
		self.coreprocessed=0









plugname="test plugin"
plugclass=PLUGIN_test_test
plugpath="test.dzup"