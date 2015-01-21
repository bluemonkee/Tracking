import sqlite3, os

def interaction2CSV(db_name, start_date, end_date, filename, count_vars, list_vars, list_purchased, count_first_free):
	

	
	#get initial connection to database
	db = sqlite3.connect("../AllDatabases/" + str(db_name))
	
	#set cursor in database
	cursor = db.cursor()
	
	#run SQL query (* is a wildcard)
	cursor.execute('SELECT * FROM kiosk_userinputs WHERE DATETIME(kiosk_userinputs.time_stamp) > \"' + str(start_date) + '\" AND DATETIME(kiosk_userinputs.time_stamp) < \"' + str(end_date) + '\"')
	
	#retrieve all results from query
	output = cursor.fetchall()
	
	# print output
	
	#empty array for results
	results = []
	
	#zero out all count_vars
	buckets = [0] * len(count_vars)
	
	#zero out all list_vars
	list_array = [] * len(list_vars)
	
	count_free = 0
			
	#print to screen
	for row in output: 
		try:
			#count count_vars
			for i in range(0,len(count_vars)):
				if str(count_vars[i]) in str(str(row[1].split(',')[0])):
					buckets[i] = buckets[i] + 1	
			
			#list list_vars
			for i in range(0,len(list_vars)):
				if str(list_vars[i]) in str(str(row[1])):
					print str(str(row[1])).replace(list_vars[i],'').replace('ValFail','').replace('MCDebit','')
					
			#count first free cards
			if count_first_free == True:
				if str(row[1].replace('  ','').split(',')[0]) == "credit":
					if str(row[2]) == "APPLIED":
						count_free = count_free + 1

			
		except: #Fail likely due to a non-unicode error
			pass
		
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
			if results[i][1].replace('  ','').split(',')[0] != "credit":
				tempArray.append(results[i][1].replace('  ','').split(',')[0])
			else:
				tempArray.append(str(str(results[i][1]).split(',')[0]) + " " + str(str(results[i][1]).split(',')[2]).rstrip())
				
				#print art printed
				if list_purchased == True:
					print str(results[i][3]) + "~" + str(results[i][1]).replace('-','').replace('MCDebit','').replace('ValFail','').replace('credit,','')
			
			#time stamp calculations
			interactionTime = abs(timeStampNow - timeStampThen)

			if interactionTime > 10 or interactionTime > 1435:
				
				tempArray.insert(0,str(results[i][4]).split('.')[0])
				tempArray.insert(0,str(len(tempArray)))
				
				
				
				#prepend lines with the following phrases
				if "Successful coupon: pennytest" in tempArray or "Successful coupon: luggage" in tempArray or "Successful coupon: connections" in tempArray:	
					tempArray.insert(0,"TESTING")
							
				elif any("credit" in array for array in tempArray):	
					tempArray.insert(0,"PURCHASE")

				else:
					# tempArray.insert(0,str(len(tempArray)))
					tempArray.insert(0,"INTERACTION")
				
				compoundArray.append(tempArray)
				tempArray = []
				
		except:
			pass

	
	emptyCount = 0
	interactionCount = 0
	
	try:
		os.remove("../AllDatabases/" + str(filename))
		# print "removed"
	except OSError as e:
		#print e
		pass
		
	for i in range(0,len(compoundArray)):
		try:
			if compoundArray[i][0] == "Hourly restart":
				emptyCount += 1
			else:
				interactionCount += 1
				with open("../AllDatabases/" + str(filename), 'a') as the_file:
					myString = "~".join(compoundArray[i] )
					the_file.write(myString)
					the_file.write('\n')
		except:
			pass
			

	
	# print interactionCount
	
	#close the database when we are done with it
	db.close()
	
	#Results for count_vars
	print "================================"
	
	if count_first_free == True:
		print "Free cards delivered = " + str(count_free)
	
	for i in range(0,len(count_vars)):
		print "String \"" + str(count_vars[i]) + "\" occurs " + str(buckets[i]) + " times"

# Start execution here!
if __name__ == '__main__':
	interaction2CSV('1stmaincardislekiosk.sqlite3','2015-01-01 0:00:00','2015-01-03 0:00:00','interaction.csv')