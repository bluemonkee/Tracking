import sqlite3
from datetime import datetime, timedelta


    
def delete_all_rows(db_name):
    
    # get initial connection to database
    db = sqlite3.connect("../AllDatabases/" + db_name)
    
    # set cursor in database
    cursor = db.cursor()
    
    # run SQL query (* is a wildcard)
    cursor.execute('DELETE FROM cycles')
    cursor.execute('DELETE FROM raw')
    cursor.execute('DELETE FROM visits')
    cursor.execute('DELETE FROM purchases')
    cursor.execute('DELETE FROM designs')
    
    db.commit() 
                
                
        
            



# Start execution here!
if __name__ == '__main__':
    print "Starting execution"
    delete_all_rows('master.sqlite3')