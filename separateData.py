import sqlite3
from datetime import datetime, timedelta
import deleteFrom


    
def separate_db_into_interactions(raw_db_name, cleaned_db_name, tag):
    
    # get initial connection to database
    db_raw = sqlite3.connect("../AllDatabases/" + raw_db_name)
    
    # set cursor in database
    cursor_raw = db_raw.cursor()
    
    # run SQL query (* is a wildcard)
    cursor_raw.execute('SELECT * FROM kiosk_userinputs')
    
    # retrieve all results from query
    output = cursor_raw.fetchall()
    # exclude non-necessary data
    excludes = ["Hourly restart", "Waiting for user to stop", "Page timeout", "First card free timed out", "Swapping default printer", "---Printer", "No prints in queue", "blank", "---Default printer", "Print command has been sent"]
    removals = []
    for index, row in enumerate(output): 
        for x in excludes:
            if x in row[1]:
                removals.append(row)
    for lines in removals:
        output.remove(lines)

    
    cursor_raw.close()
    
    
    #Connect to cleaned_db_name
    db = sqlite3.connect("../AllDatabases/" + cleaned_db_name)
    
    #set cursor in db
    cursor = db.cursor()
    
    #Get highest physical key from visits and cycles and INCREMENT
    try:
        cursor.execute('SELECT id FROM visits ORDER BY id DESC')
        visit_key = int(cursor.fetchone()[0]) + 1
    except:
        visit_key = 1
    try:
        cursor.execute('SELECT id FROM cycles ORDER BY id DESC')
        cycle_key = int(cursor.fetchone()[0]) + 1
    except:
        cycle_key = 1
    #Start activity key at 1
    design_key = 1
    purchase_key = 1

    
    #initialize
    #Create row for initial visit
    start_time = datetime.strptime(output[0][4].split('.')[0], '%Y-%m-%d %H:%M:%S')
    cursor.execute('''INSERT INTO visits(id, exit_type, kiosk_name) VALUES(?,?,?)''', (visit_key, "blank", tag))
    cursor.execute('''INSERT INTO cycles(id, id_visit, exit_type, start_time) VALUES(?,?,?,?)''', (cycle_key, visit_key, "blank", start_time))
    
    
    #Current activity (only one activity can be active at a time)
    current_activity = None
    
    #loop over all rows
    for index, row in enumerate(output):

        # previous_image = output[index][3]

        #previous, current, and next click values
        current_click = row[1].split(',')[0]
        if index == 0:
            previous_click = "blank"
        else:
            previous_click = output[index-1][1].split(',')[0]
        
        if index == len(output) - 1:
            next_click = "blank"
        else:
            next_click = output[index+1][1].split(',')[0]
        
        
        # VISIT SEPARATION
        ###############################################################
        #separation based on idle time
        current_time = datetime.strptime(output[index][4].split('.')[0], '%Y-%m-%d %H:%M:%S')
        if index == 0:
            previous_time = current_time
        else:
            previous_time = datetime.strptime(output[index-1][4].split('.')[0], '%Y-%m-%d %H:%M:%S')
        if index == len(output) - 1:
            next_time = "blank"
        else:
            next_time = datetime.strptime(output[index+1][4].split('.')[0], '%Y-%m-%d %H:%M:%S')
        time_passed = current_time - previous_time
        
        #separation based on clicks
        visit_split = False
        visit_value = "Idle time"
        visit_clicks = ["Printing finished", "Design another card clicked"]
        for split in visit_clicks:
            if split in current_click:
                visit_split = True
                visit_value = split
            if split in previous_click:
                time_passed = current_time - current_time
        # END OF VISIT SEPARATION
        ###############################################################
        
        
        
        # CYCLE SEPARATION
        ###############################################################
        #separation based on clicks
        cycle_split = False
        cycle_value = visit_value
        cycle_clicks = ["Back button to start screen", "Go home button"]
        for split in cycle_clicks:
            if split in current_click:
                cycle_split = True
                cycle_value = split
        # END OF CYCLE SEPARATION
        ###############################################################
        
        
        
        # ACTIVITY SEPARATION
        ###############################################################
        
        #activity template = ["activity_name", ["start_click1","start_click2"], ["finish_click1", finish_click2"]]
        design_activity = ["designs",["Opened", "Right inside of card clicked", "Front of card clicked",
                                      "Left inside of card clicked", "Front button clicked",
                                      "Back of card button clicked", "Inside button or suggested text clicked"],
                           ["Gray area used to close", "X button used to close", "Checkout button"]]
        purchase_activity = ["purchases",["credit","Successful coupon: luggage","Successful coupon: Coupon applied!"],["Printing finished", "Design another card clicked"]]
        ad_activity = ["ads",["Ad for"],["Ad for"]]
        # shop_activity = ["shops",["Shop"],["Shop"]]
        # preference_activity = ["preferences",["preference value"],["preference value"]]
        # top_activity = ["top_buttons",["TOP button"],["TOP button"]]
        
        
        
        activity_clicks = [design_activity, purchase_activity]#, shop_activity, preference_activity, top_activity]
        
        # Cycle through activity array
        ##------------------------------------------------------    
        activity_split_start = None
        activity_split_finish = None
        activity_finish = visit_value
        activity_start = None
        activity_type_start = None
        activity_type_finish = None
        
        
        
        for activity in activity_clicks:
            
            for split_finish in activity[2]:
                if current_activity == activity[0] and ((split_finish in current_click) or cycle_split or visit_split or time_passed > timedelta(minutes=5)):
                    activity_split_finish = True
                    activity_value_finish = split_finish
                    activity_type_finish = activity[0]
                    current_activity = None
                    if cycle_split:
                        activity_value_finish = cycle_value
                    if visit_split:
                        activity_value_finish = visit_value
                    if time_passed > timedelta(minutes=5):
                        activity_value_finish = "Idle time"
                    
            for split_start in activity[1]:
                # print "                        " + str(split_start) + "  " + str(next_click) + "   " + str(current_activity)
                if split_start in next_click and current_activity == None:
                    activity_split_start = True
                    activity_value_start = split_start
                    activity_type_start = activity[0]
                    current_activity = activity_type_start

                                        
                
        # END OF ACTIVITY SEPARATION
        ###############################################################
        
        #Activity separations
        if activity_split_finish:
        
            #Activity-specific queries
            if activity_type_finish == "designs":
                cursor.execute('''UPDATE designs SET exit_type = ?, text_selected = ? WHERE id = ?''',
                               (activity_value_finish, row[6], design_key))
                design_key = design_key + 1
            elif activity_type_finish == "purchases":
                cursor.execute('''UPDATE purchases SET exit_type = ? WHERE id = ?''',
                               (activity_value_finish, purchase_key))
                purchase_key = purchase_key + 1
            
            
            
        
        
        
        #Visit and cycle separations
        if index == len(output) - 1: #close everything upon completion
            cursor.execute('''UPDATE visits SET exit_type = ? WHERE id = ?''', (visit_value, visit_key))
            cursor.execute('''UPDATE cycles SET exit_type = ? WHERE id = ?''', (cycle_value, cycle_key))
                        
        elif time_passed > timedelta(minutes=5) or visit_split:
            cursor.execute('''UPDATE visits SET exit_type = ? WHERE id = ?''', (visit_value, visit_key))
            cursor.execute('''UPDATE cycles SET exit_type = ? WHERE id = ?''', (cycle_value, cycle_key))
            #increment keys
            visit_key = visit_key + 1
            cycle_key = cycle_key + 1
                      
            cursor.execute('''INSERT INTO visits(id, exit_type, kiosk_name) VALUES(?,?,?)''', (visit_key, "blank", tag))
            
            if cycle_value == "Idle time":
                cursor.execute('''INSERT INTO cycles(id, id_visit, exit_type, start_time) VALUES(?,?,?,?)''', (cycle_key, visit_key, "blank", current_time))
            else:
                cursor.execute('''INSERT INTO cycles(id, id_visit, exit_type, start_time) VALUES(?,?,?,?)''', (cycle_key, visit_key, "blank", next_time))
            
        elif cycle_split:
            cursor.execute('''UPDATE cycles SET exit_type = ? WHERE id = ?''', (cycle_value, cycle_key))
            cycle_key = cycle_key + 1
            
            if (next_time - current_time) < timedelta(minutes=5):
                cursor.execute('''INSERT INTO cycles(id, id_visit, exit_type, start_time) VALUES(?,?,?,?)''', (cycle_key, visit_key, "blank", next_time))
            else:
                cycle_key = cycle_key - 1

        # print "             " + str(current_click)
        # print "        " + str(activity_split_start)
        #raw clicks
        if current_click == "Printing finished" or current_click == "Design another card clicked":
            temp_visit_key = visit_key - 1
        else:
            temp_visit_key = visit_key
        cursor.execute('''INSERT INTO raw(value, start_time, id_visit) VALUES(?,?,?)''', (current_click, current_time,
                                                                                          temp_visit_key))

        if activity_split_start:
             #Activity-specific queries
            if activity_type_start == "designs":
                cover_selected = next_click.replace("Opened ","").lstrip()
                # print cover_selected
                if not len(cover_selected) > 0:
                    for i in range(-1,10):
                        cover_selected = output[index-i][3]
                        if len(cover_selected) > 0  and not cover_selected == "blank":
                            break
                cursor.execute('''INSERT INTO designs (id, exit_type, cover_selected, text_selected, start_time, id_cycle) VALUES(?,?,?,?,?,?)''', (design_key,"filler",cover_selected,"filler",next_time,cycle_key))
                
                
            elif activity_type_start == "purchases":
                try:
                    nps_score = None
                    coupon_value = "None"
                    receipt_email = "None"
                    cc_name = "None"
                    for i in range(0,10):
                        if "Net Promoter value of " in output[index+i][1].split(',')[0]:
                            nps_score = int(output[index+i][1].split(',')[0].replace("Net Promoter value of ","").lstrip())
                        elif "Successful coupon: " in output[index+i][1].split(',')[0]:
                            coupon_value =  output[index+i][1].split(',')[0].replace("Successful coupon: ","").lstrip()
                        elif "APPLIED" in output[index+i][2] and coupon_value == "None":
                            coupon_value = "FirstFree"
                        elif "credit" in output[index+i][1].split(',')[0]:
                            cc_name = output[index+i][1].split(',')[1].lstrip() + " " + output[index+i][1].split(',')[2].lstrip()
                        elif "Email receipt sent: " in output[index+i][1]:
                            receipt_email =  output[index+i][1].replace("Email receipt sent: ","").lstrip()
                        

                except:
                    pass
                cursor.execute('''INSERT INTO purchases (id, exit_type, id_design, cc_name, start_time, net_promoter_score, net_promoter_feedback, coupon_used, receipt_email, id_cycle) VALUES(?,?,?,?,?,?,?,?,?,?)''', (purchase_key, "filler", design_key - 1, cc_name, next_time, nps_score, "Not available", coupon_value, receipt_email, cycle_key))
                
            else:
                cursor.execute('''INSERT INTO ''' + activity_type_start + ''' (value, start_time, id_cycle) VALUES(?,?,?)''', (next_click,next_time,cycle_key))
                    
                
    db.commit() 
                
                
        
            



# Start execution here!
if __name__ == '__main__':
    print "Starting execution"
    deleteFrom.delete_all_rows('master.sqlite3')
    print "TABLE CLEARED"
    
    emails = ['eatscardislekiosk','techcardislekiosk','dietrickcardislekiosk','umallcardislekiosk','1stmaincardislekiosk','16westkiosk','kiosk7cardisle','pharmacycardislekiosk','metalcardislekiosk']#
    for kiosk in emails:
        separate_db_into_interactions(str(kiosk) + '.sqlite3', 'master.sqlite3', str(kiosk))