#this library should contain any functions and data needed by dezutezeoid
#that don't need to be in the actual engine executable

#some functions do rely on variables only present within DZU-ENG1.py however.
print ("dzulib initalized")
#inital main.sav file structure
savtree='''<?xml version="1.0" encoding="UTF-8"?>
<sav>
	<keysav>
	</keysav>
</sav>
'''
def initmainsave():
	print ('Initalize main.sav')
	mainsavfile = open('main.sav', 'w')
	mainsavfile.write(savtree)
	mainsavfile.close()

