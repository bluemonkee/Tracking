import sqlite3



def mergeDatabases(coreDatabase,additionalDatabase,prefix):

	print "               Appending " + str(additionalDatabase)
	
	# Get connections to the database
	db_b = sqlite3.connect("../AllDatabases/" + str(additionalDatabase))
	
	# Get contents from specified table
	##############################################
	b_cursor = db_b.cursor() #set cursor in database
	
	sqlArguement = "alter table kiosk_userinputs add column 'location' 'text' default \'" + str(prefix) + "\'"
	db_b.execute(sqlArguement) #add location column to DB
	
	b_cursor.execute('SELECT * FROM kiosk_userinputs') #wildcard selection from kiosk_userinputs
	
	output = b_cursor.fetchall()   # Returns the results as a list.
	# for row in output: #this is just a testing feature
		# print row
	b_cursor.close()
		
	# Insert these contents into another DB
	db_a = sqlite3.connect("../AllDatabases/" + str(coreDatabase))
	a_cursor = db_a.cursor()
	for row in output:
		a_cursor.execute('INSERT INTO kiosk_userinputs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', row[0:9])
		# print row
	db_a.commit()
		

def combineDB():
	print "combining..."
	#create empty DB
	myList=[1,2,3,4,5,6] #list of DB names
	myList=[1,2,3,4,5,6] #list of append names
	mergeDatabases('1stmaincardislekiosk.sqlite3','eatscardislekiosk.sqlite3','test')



# Start execution here!
if __name__ == '__main__':
	combineDB()