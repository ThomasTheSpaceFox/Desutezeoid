#!/usr/bin/env python

#wrapper plugin for dzulib's makegradient function.
class PLUGIN_gradient_gradient:
	def __init__(self, screensurf, keylist, vartree):
		self.screensurf=screensurf
		self.keylist=keylist
		#best practice to init keyid variables during init, and default them to "0" (the null keyid)
		self.keyid="0"
	def fork(self, tagobj):
		return
	def core(self, tagobj):
		if tagobj.tag=="gradient":
			self.xpos=int(tagobj.attrib.get("x"))
			self.ypos=int(tagobj.attrib.get("y"))
			self.csx=int(tagobj.attrib.get("sizex"))
			self.csy=int(tagobj.attrib.get("sizey"))
			self.rot=int(tagobj.attrib.get("rot", "0"))
			self.COL1=dzulib.colorify(tagobj.attrib.get("COLOR1", "#FFFFFF"))
			self.COL2=dzulib.colorify(tagobj.attrib.get("COLOR2", "#000000"))
			#notice how this generates a filename key and passes it to dzulib.filelookup.
			#see imageloader method below for an explanation of this plugin API feature.
			#essentially this plugin's core object uses its own fileloader API syntax.
			self.screensurf.blit(dzulib.filelookup("gradient--" + str(self.csx) + "--" + str(self.csy) + "--" + str(self.rot) + "--" + tagobj.attrib.get("COLOR1", "#FFFFFF") + "--" + tagobj.attrib.get("COLOR2", "#000000")), (self.xpos, self.ypos))
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
	#imageloader is called every time the imageloader fails to load a image file.
	#this can be used to treat the filename as a set of instructions to create an image.
	#the standard syntax should be as such: somefunction--some--variables--divided--by--two--dashes
	#the syntax of the gradient plugin is as follows:
	
	#gradient--50--60--0--#FFFFFF--#000000
	
	#the first number is x size,
	#the second is y size
	#the third is rotation degrees
	#then we have the two colors of the gradient.
	
	#for plugin writers you can use imageloader_nocache(self, filename) instead for animated generated images. this like it says, bypasses the image cache.
	#for static generated images, like this gradient plugin, use the normal imageloader(self, filename). Note that this will cache the image.
	#if you use both, ensure they have dfferent syntax. as images existing in cache means the image loader just returns the cahced version.
	def imageloader(self, filename):
		filenlist=filename.split("--")
		if filenlist[0]=="gradient":
			self.csx=int(filenlist[1])
			self.csy=int(filenlist[2])
			self.rot=int(filenlist[3])
			self.COL1=dzulib.colorify(filenlist[4])
			self.COL2=dzulib.colorify(filenlist[5])
			return pygame.transform.scale(dzulib.makegradient(self.COL1, self.COL2, self.rot), (self.csx, self.csy))
		







plugname="gradient plugin"
plugclass=PLUGIN_gradient_gradient
plugpath=None