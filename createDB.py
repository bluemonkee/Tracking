import sqlite3, shutil, time


def createDB(databaseName):

	try:
		fileParts = str(databaseName).split('.')
		shutil.move("../AllDatabases/" + str(databaseName),"../AllDatabases/backup/" + str(fileParts[0] + str(time.time()).split('.')[0].split('.')[0] + "." + fileParts[1]))
	except Exception as e:
		print e

	db = sqlite3.connect("../AllDatabases/" + str(databaseName))
	cursor = db.cursor()
	cursor.execute('''
		CREATE TABLE kiosk_userinputs(cover_text varchar(200), 
		last_click varchar(200),
		other varchar(200),
		selected_image varchar(200),
		time_stamp timestamp,
		last_url varchar(200),
		input_text varchar(200),
		id INTEGER,
		location TEXT)''')
	db.commit()


# Start execution here!
if __name__ == '__main__':
	print "Starting database creation..."
	createDB('master.sqlite3')