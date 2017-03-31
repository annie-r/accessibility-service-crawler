import time, sys, os.path, os
import subprocess #for running monkey command to start app with package name alone
sys.path.append(os.path.join('/usr/lib/python2.7/dist-packages/'))
import yaml

def yaml_loader(filepath):
	file_descriptor = open(filepath, "r")
	data = yaml.load(file_descriptor)
	return data

def get_package_info(package_info):
	f = open(package_info, 'r')
	package = f.readline().split(":")[1]
	#remove new line
	package = package[:-1]
	print "package:"
	print package
	activity = f.readline().split(":")[1]
	activity = activity[:-1]
	print "activity: "
	print activity
	f.close()
	return {'package':package, 'activity':activity}

def start_app(device, app_info):
	bashCommand = "adb shell monkey -p "+app_info['package']+" -c android.intent.category.LAUNCHER 1"
	bashCall(bashCommand)
	#runComponent = package + '/' + activity
	#device.wake()
	#print runComponent
	#runComponent = 'com.skype.raider/.Main'
	#device.startActivity(component=runComponent)
'''
def check_valid_screen(compImage):
	refFailScreensDir = './logs/failScreens'
	ref_x=0
	ref_y=20
	ref_w=240
	ref_h=3
	ACCEPTANCE = 1.0
	for refFile in os.listdir(refFailScreensDir):
		subScreen = compImage.getSubImage(ref_x, ref_y,ref_w,ref_h)
		failScreen =  MonkeyImage.loadFromFile(refFile)
		if subScreen.sameAs(reference, ACCEPTANCE):
			print "matched failScreen: " + str(refFile)
			return 1
	print "didn't match a fail screen from: " + str(refFailScreensDir)
	return 0
'''

def bashCall(bashCommand):
	print "bash Call: "+bashCommand
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	output = process.communicate()[0]
	print "output "
	print output

if __name__ == "__main__":
	print "here"
	#parse command line paramenters
	traversal_filepath = ''
	package_info = "./data/packageInfo.txt"
	logsdir=''
	num_args = len(sys.argv)
	arg_iter = 1
	is_access_service = False
	while (arg_iter < num_args):
		print "arg ", arg_iter, ": ", str(sys.argv[arg_iter])
		if sys.argv[arg_iter] == "-l":
			arg_iter += 1
			logsdir = str(sys.argv[arg_iter])
		elif sys.argv[arg_iter] == "-i":
			arg_iter += 1
			package_info = sys.argv[arg_iter]
		elif sys.argv[arg_iter] == "-t":
			arg_iter += 1
			traversal_filepath = sys.argv[arg_iter]#"C:\Users\\ansross\Documents\Research\Android_Accessability_Capture\Code\dockerEmu\\android-emulator-access\code\1traversal.yaml"
			#traversal_filepath = "code/accessSettingsTraversal.yaml"#str(sys.argv[arg_iter])
		elif sys.argv[arg_iter] == "-access":
			is_access_service = True
		else:
			print "unknown parameter flag " + sys.argv[arg_iter]
		arg_iter +=1 
	
	print "traversal filepath:", traversal_filepath
	print "logsdir:", logsdir
	print " package_info:",package_info
	print "traversing"
	count=1
	capture_count=0
	filename="screen"
	traversal_file_data = yaml_loader(traversal_filepath)
	print "traversal data: "
	print traversal_file_data
	app_info={}
	if not is_access_service:
		print "not access service"
		#get package name
		#open app
		#start_app(device, app_info)
	else:
		print "access service"
	traversal_info = traversal_file_data['traversal']
	for traversal_info_key, traversal_info_value in traversal_info.iteritems():
		print "key"
		print traversal_info_key 
		print "\nvalue:"
		print traversal_info_value
		if (traversal_info_key == "commands"):
			print "traversal info value:"
			print traversal_info_value
			for traversal_step in traversal_info_value:
				#if traversal_value == "action":
				#	action = traversal_value
				print "traversal step"
				print traversal_step
				## SET APP
				if traversal_step['type'] == "set_app":
					print "set_app"
					appName = traversal_step['app']
					print "setting app name to "+appName
					bashCommand = "adb shell am broadcast -a crawler.setApp --es appName "+appName
					bashCall(bashCommand)			
				####	
				## CLICK ###############
				elif traversal_step['type'] == "click":
					print "click"
					coords = traversal_step['coords']
					print "coords: "+str(traversal_step['coords']) 
					bashCommand = "adb shell am broadcast -a crawler.click --eia coords "+str(coords[0])+","+str(coords[1])
					bashCall(bashCommand)
				###############
				## TEXT ENTRY ############
				elif traversal_step['type'] == "text_entry":
					text = traversal_step['text']
					coords = traversal_step['coords']
					print "entering "+text+" at: "+str(coords[0])+","+str(coords[1])
					bashCommand = "adb shell am broadcast -a crawler.enterText --eia coords "+str(coords[0])+","+str(coords[1])+" --es text "+text
					bashCall(bashCommand)
				########
				## WAIT ################
				elif traversal_step['type'] == "wait":
					print "wait"
					time.sleep(traversal_step['duration'])
				## GOOGLE SCANNER CAPTURE
				elif traversal_step['type'] == "scan":
					print "scan"
					bashCommand = "adb shell am broadcast -a crawler.scan"
					bashCall(bashCommand);
    			else:
    				print "unknown type"
    				print traversal_step['type']
    			##########################
				## DRAG #####
				'''
				elif traversal_step['type'] == "drag":
					start = traversal_step['coords_start']
					end = traversal_step['coords_end']
					device.wake()
					device.drag(start, end, float(traversal_step['duration']), 5)
				## SCREENSHOT ##########
				elif traversal_step['type'] == "screenshot":
					print "screenshot"
					device.wake()
					screenShot = device.takeSnapshot()
					print "writing to : ./"+logsdir+"/"+filename+str(count)+".png"
					screenShot.writeToFile('./'+logsdir+'/'+filename+str(count)+".png",'png')
					count=count+1
				'''
				#####
    		print "end of for"
    	print "end of commands"
	print "just traversal_info:"
	print traversal_info
	print "\nend traversal"
'''

	f = open('./'+logsdir+'/traversal.txt', 'r')
	for line in f:
		coord = line.split(",")
		print "coord: x="+coord[0]+" y="+coord[1]
		device.touch(int(coord[0]),int(coord[1]),'DOWN_AND_UP')
		time.sleep(60)
		screenShot = device.takeSnapshot()
		print "writing to : ./"+logsdir+"/"+filename+str(count)+".png"
		screenShot.writeToFile('./'+logsdir+'/'+filename+str(count)+".png",'png')
		count=count+1
	f.close()
	print "traversal complete"
'''