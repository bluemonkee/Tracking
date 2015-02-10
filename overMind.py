import sqlite3
from datetime import datetime, timedelta


    
def analyze_data_from_db(db_name):
    
    #Connect to cleaned_db_name
    db = sqlite3.connect("../AllDatabases/" + db_name)
    
    #set cursor in db
    cursor = db.cursor()
    
    #Time break downs
    beginning_time = datetime.strptime("2014-11-15 00:00:00", '%Y-%m-%d %H:%M:%S') - timedelta(hours=5)
    ending_time = datetime.strptime("2015-02-11 00:00:00", '%Y-%m-%d %H:%M:%S') - timedelta(hours=5)
    delta_time = timedelta(days=1)
    
    # print timestamps across top
    print ("Location | Metric | "),
    current_time = beginning_time
    while (current_time < ending_time):
        print (str(current_time).replace(" 00:00:00","") + " | "),
        current_time = current_time + delta_time
    print ""
    
    # print "Kiosk name | Start time | End time | Total visits | Visits reaching subcategory | % | Visits reaching design | % | Visits reaching purchase | % | No design using Ads | % | No design using Shop | % | No design using shop and Ads | % | No design and Free BAR | % | No design and Free Ad | % | No design and Subcategory | % | No design and preference | % |"
    # print "----------------------------------------------------------------------------------------------------------------------------------------------"
    
    emails = ['%%','eatscardislekiosk','techcardislekiosk','dietrickcardislekiosk','umallcardislekiosk','1stmaincardislekiosk','16westkiosk','kiosk7cardisle','pharmacycardislekiosk','metalcardislekiosk']
    for kiosk in emails:
        
        # SQL queries
        total_visits = ['Total visits','SELECT Count(DISTINCT visits.id) FROM visits JOIN cycles ON visits.id = cycles.id_visit WHERE cycles.start_time > "original_time_filler" AND cycles.start_time < "current_time_filler" AND visits.kiosk_name LIKE "kiosk_name_filler"']
        visits_reaching_subcategory = ['Visits reaching subcategory','SELECT COUNT(DISTINCT raw.id_visit) FROM raw JOIN visits ON raw.id_visit = visits.id WHERE visits.kiosk_name LIKE "kiosk_name_filler" AND raw.start_time > "original_time_filler" AND raw.start_time < "current_time_filler" AND ((raw.value LIKE "%Subcategory%" OR raw.value LIKE "%Ad %" OR raw.value LIKE "%Instructions%" or raw.value LIKE "%Start shopping%") AND NOT raw.value LIKE "%Free%")']
        visits_reaching_design = ['Visits reaching design','SELECT COUNT(DISTINCT id_visit) FROM visits JOIN cycles ON visits.id = cycles.id_visit JOIN designs ON cycles.id = designs.id_cycle WHERE cycles.start_time > "original_time_filler" AND cycles.start_time < "current_time_filler" AND visits.kiosk_name LIKE "kiosk_name_filler"']
        visits_reaching_print = ['Visits reaching print','SELECT COUNT(DISTINCT id_visit) FROM visits JOIN cycles ON visits.id = cycles.id_visit JOIN purchases ON cycles.id = purchases.id_cycle WHERE NOT coupon_used = "pennytest" AND NOT coupon_used = "luggage" AND cycles.start_time > "original_time_filler" AND cycles.start_time < "current_time_filler" AND visits.kiosk_name LIKE "kiosk_name_filler"']
        visits_reaching_purchase = ['Visits reaching purchase','SELECT COUNT(DISTINCT id_visit) FROM visits JOIN cycles ON visits.id = cycles.id_visit JOIN purchases ON cycles.id = purchases.id_cycle WHERE NOT coupon_used = "pennytest" AND NOT coupon_used = "luggage" AND NOT coupon_used = "FirstFree" AND cycles.start_time > "original_time_filler" AND cycles.start_time < "current_time_filler" AND visits.kiosk_name LIKE "kiosk_name_filler"']
        
        
        all_queries = [total_visits, visits_reaching_subcategory, visits_reaching_design, visits_reaching_print, visits_reaching_purchase]
        
        for query in all_queries:
            if kiosk == "%%":
                    print ("everything | " + query[0] + " | "),
            else:
                print (kiosk + " | " + query[0] + " | "),
            current_time = beginning_time
            while (current_time < ending_time):
                
                original_time = current_time
                current_time = current_time + delta_time

                cursor.execute(query[1].replace('original_time_filler',str(original_time)).replace('current_time_filler',str(current_time)).replace('kiosk_name_filler',kiosk))
                metric_counts = cursor.fetchone()
                print ( str(metric_counts[0])+ " | "),
                
            print ""
        if kiosk == '%%':
            print "\n\n\n\n"
        
    
    
    
    db.commit() 
                
                
        
            



# Start execution here!
if __name__ == '__main__':
    # print "Starting execution"
    analyze_data_from_db('master.sqlite3')
