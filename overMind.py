#in house libraries
import fileBackup
import downloadAttachments
import combineDatabases
import createDB
import interactionCSV

#Create folder \Github\AllDatabases\backup



# Start date and end date for analysis# 
start_date = '2015-01-10 0:00:00'
end_date = '2015-01-15 0:00:00'

# Download latest databases and replace existing?
new_databases = True

# Create CSV of interactions?
new_csv = True

# List purchased art
list_purchased = True

# Count occurrences of count_vars 
count_vars = ["credit", "pennytest", "luggage", "parade", "imissmom"]

# List variable following string
list_vars = []

# Count occurrences of sequence of events

# List variable following sequence of strings


# all kiosks
all_kiosks = ['eatscardislekiosk', 'techcardislekiosk', 'dietrickcardislekiosk', 'umallcardislekiosk', '1stmaincardislekiosk', '16westkiosk', 'kiosk7cardisle', 'pharmacycardislekiosk', 'metalcardislekiosk', 'master']

# Start execution here!
if __name__ == '__main__':

		# UPDATE MASTER DB# 
	# --------------------------------------------# 
	
	if new_databases == True:
		# Create blank master DB# 
		createDB.createDB('master.sqlite3')

		for address in all_kiosks[:-1]:
			# Backing up databases# 
			fileBackup.backingUp(str(address) + ".sqlite3")
			
			# Downloading new databases# 
			password = '5408675309'
			if address == 'eatscardislekiosk' or address == 'techcardislekiosk':
				password = 'Bettergr33tings'
			downloadAttachments.downloadAttachments(str(address) + "@gmail.com", password)
				
			# Combine databases# 
			combineDatabases.mergeDatabases('master.sqlite3',str(address) + ".sqlite3",str(address))
	# --------------------------------------------# 

	for kiosk in all_kiosks:
		print "\n\n\n------------------------------"
		print kiosk
		print "----------------------------------"
		# ANALYZE DB# 
		# --------------------------------------------# 		
		if new_csv == True:
			#Create csv of interactions
			interactionCSV.interaction2CSV(str(database_name) + '.sqlite3', start_date, end_date, new_csv_filename, count_vars, list_vars, list_purchased)
		print "--------------------------------"
		
		
		
		