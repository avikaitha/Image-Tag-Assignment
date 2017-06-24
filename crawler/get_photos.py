import psycopg2
import urllib2
import os
import traceback
"""
URL Format:
https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{o-secret}_o.(jpg|gif|png)
https://farm6.staticflickr.com/5345/31333748230_99cba0512d.jpg
"""
def get_image(url, image_save_name):
    try:
        image = urllib2.urlopen(url).read()
        with open(image_save_name + '.' + url.split('.')[-1], 'wb') as image_file:
            image_file.write(image)
            image_file.close()
    except Exception as e:
        print e

try:
    conn = psycopg2.connect("dbname='flickr2' user='postgres' host='129.219.60.22' password='password'")
    print "Successfully connected...."
except:
    pass

cur = conn.cursor()

import csv
fil = open('usrid_new.csv','rb')
records = csv.reader(fil)
records = list(records)
records = records[1:]

for record in records:
    user_id = record[0]
    # user_id = '62202285@N00'
    file_path = "C:\\Users\\akaitha\\PycharmProjects\\flickr_crawler\\images_150X150\\"+user_id+"\\"
    # print file_path
    directory = os.path.dirname(file_path)
    os.makedirs(directory)
    # if not os.path.exists(directory):
    #     print "Test"

    st = "select * from image_download_metadata where owner = '"+user_id+"'"
    try:
        cur.execute(st)

        image_metadata = cur.fetchall()
        count = 0
        for data in image_metadata:
            farm_id = data[4]
            server_id = data[3]
            id = data[0]
            secret = data[2]

            url = "https://farm"+farm_id+".staticflickr.com/"+server_id+"/"+id+"_"+secret+"_q.jpg"
            get_image(url,"images_150X150\\"+user_id+"\\"+id)
            count += 1

            if count%100 == 0:
                print "Current count: ",count


        print user_id,": ",len(data)
    except:
        traceback.print_exc()








