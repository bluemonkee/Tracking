import sqlite3
from datetime import datetime, timedelta


    
def analyze_data_from_db(db_name):
    
    #Connect to cleaned_db_name
    db = sqlite3.connect("../AllDatabases/" + db_name)
    
    #set cursor in db
    cursor = db.cursor()
    
    #Time break downs
    beginning_time = datetime.strptime("2014-11-15 00:00:00", '%Y-%m-%d %H:%M:%S')
    ending_time = datetime.strptime("2015-01-31 00:00:00", '%Y-%m-%d %H:%M:%S')
    delta_time = timedelta(days=7)
    
    print "Kiosk name | Start time | End time | Total visits | Visits reaching subcategory | % | Visits reaching design | % | Visits reaching purchase | % | No design using Ads | % | No design using Shop | % | No design using shop and Ads | % | No design and Free BAR | % | No design and Free Ad | % | No design and Subcategory | % | No design and preference | % |"
    print "----------------------------------------------------------------------------------------------------------------------------------------------"
    
    emails = ['eatscardislekiosk','techcardislekiosk','dietrickcardislekiosk','umallcardislekiosk','1stmaincardislekiosk','16westkiosk','kiosk7cardisle','pharmacycardislekiosk','metalcardislekiosk','%%']
    for kiosk in emails:
        
        current_time = beginning_time
        while (current_time < ending_time):
            if kiosk == "%%":
                print ("everything | "),
            else:
                print (kiosk + " | "),
            original_time = current_time
            current_time = current_time + delta_time
            #Print dates
            print (str(original_time) + " | " + str(current_time) + " | "),
            # Total visits
            cursor.execute('SELECT Count(DISTINCT visits.id) FROM visits JOIN cycles ON visits.id = cycles.id_visit WHERE cycles.start_time > \"' + str(original_time) + '\"AND cycles.start_time < \"' + str(current_time) + '\" AND visits.kiosk_name LIKE \"' + kiosk + '\"')
            visits_counted = cursor.fetchone()
            #Print total visits
            print ( str(visits_counted[0])+ " | "),
            
            # Visits reaching subcategory
            cursor.execute('SELECT COUNT(DISTINCT raw.id_visit) FROM raw JOIN visits ON raw.id_visit = visits.id WHERE visits.kiosk_name LIKE \"' + kiosk + '\" AND raw.start_time > \"' + str(original_time) + '\" AND raw.start_time < \"' + str(current_time) + '\" AND ((raw.value LIKE "%Subcategory%" OR raw.value LIKE "%Ad %") AND NOT raw.value LIKE "%Free%")')
            subcategories_counted = cursor.fetchone()
            #Print visits reaching design
            try:
                print (str(subcategories_counted[0]) + " | " + str(100 * subcategories_counted[0]/visits_counted[0]) + "% | "),
            except:
                print (str(subcategories_counted[0]) + " | 0% | "),
            
            # Visits reaching design
            cursor.execute('SELECT COUNT(DISTINCT id_visit) FROM visits JOIN cycles ON visits.id = cycles.id_visit JOIN designs ON cycles.id = designs.id_cycle WHERE cycles.start_time > \"' + str(original_time) + '\" AND cycles.start_time < \"' + str(current_time) + '\" AND visits.kiosk_name LIKE \"' + kiosk + '\"')
            designs_counted = cursor.fetchone()
            #Print visits reaching design
            try:
                print (str(designs_counted[0]) + " | " + str(100 * designs_counted[0]/visits_counted[0]) + "% | "),
            except:
                print (str(designs_counted[0]) + " | 0% | "),
            
            # Visits reaching purchase
            cursor.execute('SELECT COUNT(DISTINCT id_visit) FROM visits JOIN cycles ON visits.id = cycles.id_visit JOIN purchases ON cycles.id = purchases.id_cycle WHERE NOT coupon_used = "pennytest" AND NOT coupon_used = "luggage" AND cycles.start_time > \"' + str(original_time) + '\" AND cycles.start_time < \"' + str(current_time) + '\" AND visits.kiosk_name LIKE \"' + kiosk + '\"')
            purchases_counted = cursor.fetchone()
            try:
                print (str(purchases_counted[0]) + " | " + str(100 * purchases_counted[0]/visits_counted[0]) + "% | "),
            except:
                print (str(purchases_counted[0]) + " | 0% | "),
            
            # Ad used to open and design not reached
            cursor.execute('SELECT COUNT(DISTINCT visits.id) FROM visits JOIN cycles ON visits.id = cycles.id_visit JOIN raw ON visits.id = raw.id_visit LEFT JOIN designs ON cycles.id = designs.id_cycle WHERE designs.id_cycle IS NULL AND raw.value LIKE "%Ad%" AND cycles.start_time > \"' + str(original_time) + '\" AND cycles.start_time < \"' + str(current_time) + '\" AND visits.kiosk_name LIKE \"' + kiosk + '\"')
            ad_with_no_designs_counted = cursor.fetchone()
            try:
                print (str(ad_with_no_designs_counted[0]) + " | " + str(100 * ad_with_no_designs_counted[0]/visits_counted[0]) + "% | "),
            except:
                print (str(ad_with_no_designs_counted[0]) + " | 0% | "),
                
            # Shop used to open and design not reached
            cursor.execute('SELECT COUNT(DISTINCT visits.id) FROM visits JOIN cycles ON visits.id = cycles.id_visit JOIN raw ON visits.id = raw.id_visit LEFT JOIN designs ON cycles.id = designs.id_cycle WHERE designs.id_cycle IS NULL AND raw.value LIKE "%Shop%" AND cycles.start_time > \"' + str(original_time) + '\" AND cycles.start_time < \"' + str(current_time) + '\" AND visits.kiosk_name LIKE \"' + kiosk + '\"')
            shop_with_no_designs_counted = cursor.fetchone()
            try:
                print (str(shop_with_no_designs_counted[0]) + " | " + str(100 * shop_with_no_designs_counted[0]/visits_counted[0]) + "% | "),
            except:
                print (str(shop_with_no_designs_counted[0]) + " | 0% | "),
                
            # Ad and shop used to open and design not reached
            cursor.execute('SELECT COUNT(DISTINCT visits.id) FROM visits JOIN cycles ON visits.id = cycles.id_visit JOIN raw ON visits.id = raw.id_visit LEFT JOIN designs ON cycles.id = designs.id_cycle WHERE designs.id_cycle IS NULL AND raw.value LIKE "%Ad%" AND raw.value LIKE "%Shop%" AND cycles.start_time > \"' + str(original_time) + '\" AND cycles.start_time < \"' + str(current_time) + '\" AND visits.kiosk_name LIKE \"' + kiosk + '\"')
            shop_and_ad_with_no_designs_counted = cursor.fetchone()
            try:
                print (str(shop_and_ad_with_no_designs_counted[0]) + " | " + str(100 * shop_and_ad_with_no_designs_counted[0]/visits_counted[0]) + "% | "),
            except:
                print (str(shop_and_ad_with_no_designs_counted[0]) + " | 0% | "),
                
            # First Free BAR used and design not reached
            cursor.execute('SELECT COUNT(DISTINCT visits.id) FROM visits JOIN cycles ON visits.id = cycles.id_visit JOIN raw ON visits.id = raw.id_visit LEFT JOIN designs ON cycles.id = designs.id_cycle WHERE designs.id_cycle IS NULL AND raw.value LIKE "%BAR%" AND cycles.start_time > \"' + str(original_time) + '\" AND cycles.start_time < \"' + str(current_time) + '\" AND visits.kiosk_name LIKE \"' + kiosk + '\"')
            free_bar_with_no_designs_counted = cursor.fetchone()
            try:
                print (str(free_bar_with_no_designs_counted[0]) + " | " + str(100 * free_bar_with_no_designs_counted[0]/visits_counted[0]) + "% | "),
            except:
                print (str(free_bar_with_no_designs_counted[0]) + " | 0% | "),    
               
            # First Free Ad used and design not reached
            cursor.execute('SELECT COUNT(DISTINCT visits.id) FROM visits JOIN cycles ON visits.id = cycles.id_visit JOIN raw ON visits.id = raw.id_visit LEFT JOIN designs ON cycles.id = designs.id_cycle WHERE designs.id_cycle IS NULL AND raw.value LIKE "%Ad for Free card%" AND cycles.start_time > \"' + str(original_time) + '\" AND cycles.start_time < \"' + str(current_time) + '\" AND visits.kiosk_name LIKE \"' + kiosk + '\"')
            free_ad_with_no_designs_counted = cursor.fetchone()
            try:
                print (str(free_ad_with_no_designs_counted[0]) + " | " + str(100 * free_ad_with_no_designs_counted[0]/visits_counted[0]) + "% | "),
            except:
                print (str(free_ad_with_no_designs_counted[0]) + " | 0% | "),   
            
            # Subcategory used and design not reached
            cursor.execute('SELECT COUNT(DISTINCT visits.id) FROM visits JOIN cycles ON visits.id = cycles.id_visit JOIN raw ON visits.id = raw.id_visit LEFT JOIN designs ON cycles.id = designs.id_cycle WHERE designs.id_cycle IS NULL AND raw.value LIKE "%Subcategory%" AND cycles.start_time > \"' + str(original_time) + '\" AND cycles.start_time < \"' + str(current_time) + '\" AND visits.kiosk_name LIKE \"' + kiosk + '\"')
            subcategory_with_no_designs_counted = cursor.fetchone()
            try:
                print (str(subcategory_with_no_designs_counted[0]) + " | " + str(100 * subcategory_with_no_designs_counted[0]/visits_counted[0]) + "% | "),
            except:
                print (str(subcategory_with_no_designs_counted[0]) + " | 0% | "),
             
            # preference used and design not reached
            cursor.execute('SELECT COUNT(DISTINCT visits.id) FROM visits JOIN cycles ON visits.id = cycles.id_visit JOIN raw ON visits.id = raw.id_visit LEFT JOIN designs ON cycles.id = designs.id_cycle WHERE designs.id_cycle IS NULL AND raw.value LIKE "%preference%" AND cycles.start_time > \"' + str(original_time) + '\" AND cycles.start_time < \"' + str(current_time) + '\" AND visits.kiosk_name LIKE \"' + kiosk + '\"')
            preference_with_no_designs_counted = cursor.fetchone()
            try:
                print (str(preference_with_no_designs_counted[0]) + " | " + str(100 * preference_with_no_designs_counted[0]/visits_counted[0]) + "% | "),
            except:
                print (str(preference_with_no_designs_counted[0]) + " | 0% | "),             
            
            print ""
    
    
    
    
    
    db.commit() 
                
                
        
            



# Start execution here!
if __name__ == '__main__':
    print "Starting execution"
    analyze_data_from_db('master.sqlite3')
