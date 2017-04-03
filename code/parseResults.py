#TYPES:
#content labels
#touch target size
#Clickable items
#text contrast
#image contrast

import sys

class AppResults:
	def __init__(self,name,package):
		self.appName = name
		self.package = package
		self.errors = dict()
	#def __init__(self):
		#self.errors = dict()
	def setPackage(self, package):
		self.package = package
	def setName(self,name):
		self.appName=name
	def addError(self,error):
		#remove new line
		error = error[:-1]
		if self.errors.has_key(error):
			self.errors[error] +=1
		else:
			self.errors[error] = 1
	def getPackage(self):
		return self.package
	def printErrors(self):
		print "errors: " 
		print self.errors


if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "python parseResult <appName> <packageName>"
		sys.exit(0)
	name=sys.argv[1]
	pkg=sys.argv[2]
	result = AppResults(name,pkg)

	path="/Users/annieross/Documents/Work/EpiPaper/CrawlerResults/Scand/Pandora.2017.03.28.15.26.26/report_Pandora_2017-03-28-15-25-57.txt"
	
	#pandora = AppResults("Pandora","com.pandora.android")
	print path
	f = open(path,'r')
	prior_line = ""
	for line in f:
		print line
		package_test = line.split(":",1)
		print "package test: "+package_test[0]
		if package_test[0] == result.getPackage():
			result.addError(prior_line)
		prior_line = line
		print "BREAK"
	result.printErrors()