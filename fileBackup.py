import shutil, time


def backingUp(fileName):
	print "     Backing up " + str(fileName)
	try:
		fileParts = str(fileName).split('.')
		shutil.copy2("../AllDatabases/" + str(fileName),"../AllDatabases/backup/" + str(fileParts[0] + str(time.time()).split('.')[0].split('.')[0] + "." + fileParts[1]))
	except:
		print "     File: " + str(fileName) + " does not exist (no backup necessary)"
	

# Start execution here!
if __name__ == '__main__':
	print "Beginning..."
	backingUp('16westkiosk.sqlite3')