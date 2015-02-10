import sqlite3
import shutil
import time


def create_blank_tracking_db(database_name):

    # If database already exists, we want to create a backup
    try:
        file_parts = str(database_name).split('.')
        shutil.move("../AllDatabases/" + str(database_name), "../AllDatabases/backup/"
                    + str(file_parts[0] + str(time.time()).split('.')[0].split('.')[0] + "." + file_parts[1]))
        print "Database has been backed up."
    except:
        print "Creating new database."

    db = sqlite3.connect("../AllDatabases/" + str(database_name))
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE visits(id INTEGER,
        exit_type TEXT,
        kiosk_name TEXT)''')
    cursor.execute('''
        CREATE INDEX index_visits1 ON visits (id)''')
    cursor.execute('''
        CREATE INDEX index_visits2 ON visits (exit_type)''')
    cursor.execute('''
        CREATE INDEX index_visits3 ON visits (kiosk_name)''')

    cursor.execute('''
        CREATE TABLE cycles(id INTEGER,
        exit_type TEXT,
        start_time TIMESTAMP,
        id_visit INTEGER,
        FOREIGN KEY(id_visit) REFERENCES visits(id))''')
    cursor.execute('''
        CREATE INDEX index_cycles1 ON cycles (id)''')
    cursor.execute('''
        CREATE INDEX index_cycles2 ON cycles (exit_type)''')
    cursor.execute('''
        CREATE INDEX index_cycles3 ON cycles (start_time)''')
    cursor.execute('''
        CREATE INDEX index_cycles4 ON cycles (id_visit)''')

    cursor.execute('''
        CREATE TABLE designs(id INTEGER,
        exit_type TEXT,
        cover_selected TEXT,
        text_selected TEXT,
        start_time TIMESTAMP,
        id_cycle INTEGER,
        FOREIGN KEY(id_cycle) REFERENCES cycles(id))''')
    cursor.execute('''
        CREATE INDEX index_designs1 ON designs (id)''')
    cursor.execute('''
        CREATE INDEX index_designs2 ON designs (id_cycle)''')
    cursor.execute('''
        CREATE INDEX index_designs3 ON designs (exit_type)''')
    cursor.execute('''
        CREATE INDEX index_designs4 ON designs (cover_selected)''')
    cursor.execute('''
        CREATE INDEX index_designs5 ON designs (text_selected)''')
    cursor.execute('''
        CREATE INDEX index_designs6 ON designs (start_time)''')

        

    cursor.execute('''
        CREATE TABLE purchases(id INTEGER,
        exit_type TEXT,
        id_design,
        cc_name TEXT,
        start_time TIMESTAMP,
        net_promoter_score INTEGER,
        net_promoter_feedback TEXT,
        coupon_used TEXT,
        receipt_email TEXT,
        id_cycle INTEGER,
        FOREIGN KEY(id_design) REFERENCES designs(id),
        FOREIGN KEY(id_cycle) REFERENCES cycles(id))''')
    cursor.execute('''
        CREATE INDEX index_purchases ON purchases (id, id_cycle)''')

    cursor.execute('''
        CREATE TABLE ads(value TEXT,
        start_time TIMESTAMP,
        id_cycle INTEGER,
        FOREIGN KEY(id_cycle) REFERENCES cycles(id))''')

    cursor.execute('''
        CREATE TABLE shops(value TEXT,
        start_time TIMESTAMP,
        id_cycle INTEGER,
        FOREIGN KEY(id_cycle) REFERENCES cycles(id))''')

    cursor.execute('''
        CREATE TABLE preferences(value TEXT,
        start_time TIMESTAMP,
        id_cycle INTEGER,
        FOREIGN KEY(id_cycle) REFERENCES cycles(id))''')

    cursor.execute('''
        CREATE TABLE top_buttons(value TEXT,
        start_time TIMESTAMP,
        id_cycle INTEGER,
        FOREIGN KEY(id_cycle) REFERENCES cycles(id))''')

    cursor.execute('''
        CREATE TABLE raw(value TEXT,
        start_time TIMESTAMP,
        id_visit INTEGER,
        FOREIGN KEY(id_visit) REFERENCES visits(id))''')
    cursor.execute('''
        CREATE INDEX index_raw1 ON raw (value)''')
    cursor.execute('''
        CREATE INDEX index_raw2 ON raw (start_time)''')
    cursor.execute('''
        CREATE INDEX index_raw3 ON raw (id_visit)''')

    db.commit()


# Start execution here!
if __name__ == '__main__':
    print "Starting database creation..."
    create_blank_tracking_db('master.sqlite3')