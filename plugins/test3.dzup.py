#!/usr/bin/env python

class PLUGIN_test_test2:
	def __init__(self, screensurf, keylist, vartree):
		self.screensurf=screensurf
		self.keylist=keylist
		self.rectlist=[]
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
		if tagobj.tag=="test3":
			self.xpos=int(tagobj.attrib.get("x"))
			self.ypos=int(tagobj.attrib.get("y"))
			self.testval=(tagobj.attrib.get("testval"))
			#note: these core object tests are in red
			self.testrect=pygame.Rect(self.xpos, self.ypos, 60, 20)
			pygame.draw.rect(self.screensurf, (255, 0, 0), self.testrect)
			#ctreport is a dzulib clicktab wrapper function for when just the
			#pump/clickreturn click reporting functionality is needed.
			self.rectlist.extend([dzulib.ctreport(self.testrect, self, self.testval)])
	#called every loop. 
	def pump(self):
		self.returnlist=self.rectlist
		self.rectlist=[]
		return self.returnlist
	#called on pygame mousebuttondown events
	def click(self, event):
		return
	#called on pygame mousebuttonup events
	def clickup(self, event):
		return
	#called upon page load
	def pageclear(self):
		return
	#this is only needed when the "report" reftype is used. 
	#(note: if using clicktab directly, ref should be defined as self!)
	def clickreport(self, clickinst):
		print clickinst.data









plugname="test plugin2"
plugclass=PLUGIN_test_test2
plugpath=None