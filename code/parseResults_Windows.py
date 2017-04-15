#TYPES:
#content labels
#touch target size
#Clickable items
#text contrast
#image contrast


#7z e * -r   -oReports from *.txt Scans\Thing file
import sys, os
import subprocess

class AppResults:
	def __init__(self,name,category,package=""):
		self.appName = name
		self.package = package
		self.errors = dict()
		self.category = category
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
		print self.appName + " errors: " 
		print self.errors
	def printToFile(self,filepath):
		with open(filepath,"a") as f:
			for error in self.errors:
				f.write(self.category+","+self.appName+","+error+'\n')
		f.close()




def bashCall(bashCommand):
	print "bash Call: "+bashCommand
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	output = process.communicate()[0]
	print "output "
	print output

def unzipDirectory(directory):
	bashCommand = "7z e * -o"+directory+"\Reports *.txt"
	bashCall(bashCommand)
	print "unzip " + directory

def unzipReport (filepath,directory):
	bashCommand = "7z e \""+filepath+"\" -o"+directory+"\Reports *.txt"
	bashCall(bashCommand)
	print "unzip " + filepath


def unzipAll(directory):
	pastRoot=False
	for subdir, dirs, files in os.walk(directory):
		'''
		if pastRoot:
			bashCommand = "mkdir "+subdir+"\Reports"
			unzipDirectory(subdir)
		#print "subdir: " + os.path.join(subdir)
		'''
		print "subdir: " + os.path.join(subdir)
		for file in files:
			#print "subdir: "+subdir
			#bashCommand="mkdir \""+os.path.join(subdir)+"\Reports\""
			#bashCall(bashCommand)
			#if not os.path.isdir(subdir+"\Reports"):
				#bashCommand = "mkdir Reports"
				#bashCall(bashCommand)
			#print "join: " + os.path.join(subdir, file)
			filepath = subdir + os.sep + file
			file_name = os.sep+file
			print "file: "+file
			print "name: "+file_name
			#print "filepath: "+filepath
			if filepath.endswith(".zip"):
				unzipReport(file,subdir)
				print "zips : "+filepath
				print "subdir: "+subdir
			    #print (filepath)
		'''
		if subdir == directory:
			print "directory subdir: "+subdir
			pastRoot = True
		'''


def extractResults(directory,category,results):
	# key: app name 
	# value: AppResults	results = dict()
	for subdir, dirs, files in os.walk(directory):
		for file in files:
			name=file.split("_")[1]
			if not results.has_key(name):
				result=AppResults(name,category)
				results[name]=result
			filepath = subdir + os.sep + file
			f = open(filepath, 'r')
			try:
				while True:
					line = f.next()
					if line == '\n':
						error = f.next()
						results[name].addError(error)
			except StopIteration:
				print "done with "+filepath
			f.close()
	for name in results:
		results[name].printErrors()


	'''
	if len(sys.argv) < 3:
		print "python parseResult <appName> <packageName>"
		sys.exit(0)
	name=sys.argv[1]
	pkg=sys.argv[2]
	result = AppResults(name,pkg)

	path="C:\Users\\ansross\Documents\Research\Android_Accessability_Capture\Accessibility Scanner Results- FOX NOW - 2017-04-14-12-13-41\\report_FOX NOW_2017-04-14-12_13_41.txt"
	
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
	'''

if __name__ == "__main__":
	#rootdirectory = "C:\Users\\ansross\Documents\Research\Android_Accessability_Capture\Scans\\"
	#unzipAll(rootdirectory)
	# key: app name 
	# value: AppResults	
	results = dict()
	for subdir, dirs, files in os.walk("C:\Users\\ansross\Documents\Research\Android_Accessability_Capture\Scans"):
		print "sub: "+subdir
		directory_list = subdir.split(os.sep)
		if directory_list[-1] == "Reports":
			print directory_list[-2]
			extractDir = subdir
			category = directory_list[-2]
			extractResults(extractDir,category,results)
	resultsFile = "C:\Users\\ansross\Documents\Research\Android_Accessability_Capture\Scans\\results.csv"
	for name in results:
		results[name].printToFile(resultsFile)







