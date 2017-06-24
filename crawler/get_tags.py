import psycopg2
import urllib2
import os
import traceback
import flickrapi
import json
import threading
"""
URL Format:
https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{o-secret}_o.(jpg|gif|png)
https://farm6.staticflickr.com/5345/31333748230_99cba0512d.jpg
"""
def addslashes(s):
    d = {'"':'\\"', "'":"''", "\0":"\\\0", "\\":"\\\\"}
    return ''.join(d.get(c, c) for c in s)



def get_tags(api_key,api_secret,record):
    try:
        conn = psycopg2.connect("dbname='flickr2' user='postgres' host='129.219.60.22' password='password'")
        # print "Successfully connected...."
    except:
        pass

    cur = conn.cursor()
    flickr = flickrapi.FlickrAPI(api_key, api_secret,format='json')
    user_id = record[0]

    st = "select * from image_download_metadata where owner = '"+user_id+"'"
    try:
        cur.execute(st)

        records = cur.fetchall()
        count = 0
        for record in records:
            photo_id = record[0]
            try:
                photo_metadata = json.loads(flickr.photos.getInfo(photo_id=photo_id))
                tags = photo_metadata['photo']['tags']['tag']
                # print photo_id,tags
                for tag in tags:
                    tag_id = tag['id']
                    raw_tag = tag['raw']
                    cleaned_tag = tag['_content']

                    st = "Insert into image_tags(tag_id,photo_id,owner,raw_tag,cleaned_tag) values ('"+tag_id+"','"\
                    +photo_id+"','"\
                    +user_id+"','"\
                    +addslashes(raw_tag)+"','"\
                    +addslashes(cleaned_tag)+"')"

                    # print st
                    try:
                        cur.execute(st)
                        conn.commit()
                    except:
                        # traceback.print_exc()
                        conn.rollback()

                count += 1
            except:
                traceback.print_exc()

        print user_id,": ",len(records)
    except:
        traceback.print_exc()

    conn.close()

def main():
    count = 0



    api_keys = [u'50447f832b7d99785ebb9ba9b69e6a65',u'82764a924643a98e49381f5f28a9a5a7',u'36eadd83335122d888da119424854efc',u'51da9f4ccbd1dae169eb1e619690530e',u'5ebfd342ebab8ea6b16fbbfe6daf632e']
    api_secrets = [u'11d5ef95815b96b0',u'39c68f2dd019d2c0',u'2bbc80b7476185c5',u'5c473c8f547f07d6',u'1e9c1b2440923add']
    # api_key = u'50447f832b7d99785ebb9ba9b69e6a65'
    # api_secret = u'11d5ef95815b96b0'

    import csv
    fil = open('new_users.csv', 'rb')
    records = csv.reader(fil)
    records = list(records)
    records = records[1:]

    num_threads = 10
    while count < len(records):
        if threading.active_count() <= num_threads:
            print count
            print "Number of threads: ",threading.active_count()

            t = threading.Thread(target=get_tags,args=(api_keys[count%5],api_secrets[count%5],records[count]))
            t.start()
            count += 1
if __name__ == '__main__':
    main()








