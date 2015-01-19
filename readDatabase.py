import sqlite3, os

def readDB(db_name):
	
	#get initial connection to database
	db = sqlite3.connect(db_name)
	
	#set cursor in database
	cursor = db.cursor()
	
	#run SQL query (* is a wildcard)
	cursor.execute('SELECT * FROM kiosk_userinputs WHERE DATETIME(kiosk_userinputs.time_stamp) < "2015-01-01 0:00:00"')
	
	#retrieve all results from query
	output = cursor.fetchall()
	
	#beginning and end times
	print "STARTING: " + str(output[0][4].split('.')[0])
	print "ENDING: " + str(output[-1][4].split('.')[0])
	
	#empty array for results
	results = []
	
	#print to screen
	for row in output[0:100]: 
		# print row
		
		#identify whether event should be recorded
		try:
			test_var = row[1].split()[0]
			if test_var != "Multiple" and test_var != "blank" and test_var !=  "---Printer" and test_var !=  "No" and test_var !=  "Touch" and test_var !=  "Swapping" and test_var !=  "Hourly" and test_var !=  "---Default":
				results.append(row) #append entire row to results array if it meets criterion
		except:
			pass
			
	#Identify interactions
	######################################################
	#Interactions are separted by either >5 min or timeout
	tempArray = []
	compoundArray = []	
	for i in range(0,len(results)-1):
		try:
			#time stamp values
			timeStampRawNow = results[i][4].split(' ')[1].split('.')[0].split(':')
			timeStampRawThen = results[i+1][4].split(' ')[1].split('.')[0].split(':')
			timeStampNow = int(timeStampRawNow[0])*60 + int(timeStampRawNow[1])
			timeStampThen = int(timeStampRawThen[0])*60 + int(timeStampRawThen[1])		
			tempArray.append(results[i][1].replace('  ','').split(',')[0])
			
			#time stamp calculations
			interactionTime = abs(timeStampNow - timeStampThen)
			if interactionTime > 10 or interactionTime > 1435:
			
				#prepend lines with the following phrases
				if "Successful coupon: pennytest" in tempArray or "Successful coupon: luggage" in tempArray or "Successful coupon: connections" in tempArray:	
					tempArray.insert(0,str(len(tempArray)))
					tempArray.insert(0,"TESTING")
					compoundArray.append(tempArray)
					tempArray = []		
				elif "credit" in tempArray:	
					tempArray.insert(0,str(len(tempArray)))
					tempArray.insert(0,"PURCHASE")
					compoundArray.append(tempArray)
					tempArray = []
				else:
					tempArray.insert(0,str(len(tempArray)))
					tempArray.insert(0,"INTERACTION")
					compoundArray.append(tempArray)
					tempArray = []
				
		except:
			pass

	
	emptyCount = 0
	interactionCount = 0
	
	try:
		os.remove('cleaned.txt')
		print "removed"
	except OSError as e:
		#print e
		pass
		
	for i in range(0,len(compoundArray)):
		if compoundArray[i][0] == "Hourly restart":
			emptyCount += 1
		else:
			interactionCount += 1
			with open('cleaned.txt', 'a') as the_file:
				myString = "~".join(compoundArray[i] )
				the_file.write(myString)
				the_file.write('\n')
			

	
	print interactionCount
		
		
	
	#close the database when we are done with it
	db.close()

# Start execution here!
if __name__ == '__main__':
	readDB('kiosk7cardisle.sqlite3')