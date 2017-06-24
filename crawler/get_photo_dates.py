import flickrapi
import psycopg2
import threading
import traceback
from ast import literal_eval
import json

def data_walker(method, searchstring='*/photo', **params):
    """Calls 'method' with page=0, page=1 etc. until the total
    number of pages has been visited. Yields the photos
    returned.

    Assumes that ``method(page=n, **params).findall(searchstring)``
    results in a list of interesting elements (defaulting to photos),
    and that the toplevel element of the result contains a 'pages'
    attribute with the total number of pages.
    """

    page = 1
    total = 1  # We don't know that yet, update when needed
    while page <= total:
        # Fetch a single page of photos
        # LOG.debug('Calling %s(page=%i of %i, %s)' %
        #           (method.func_name, page, total, params))
        rsp = method(page=page, **params)
        photoset = rsp.getchildren()[0]
        total = int(photoset.get('pages'))

        photos = rsp.findall(searchstring)

        # Yield each photo
        for photo in photos:
            yield photo

        # Ready to get the next page
        page += 1

def addslashes(s):
    d = {'"':'\\"', "'":"''", "\0":"\\\0", "\\":"\\\\"}
    return ''.join(d.get(c, c) for c in s)


def get_image_loc(api_key,api_secret,record,out_file):
    # try:
    #     conn = psycopg2.connect("dbname='flickr2' user='postgres' host='129.219.60.22' password='password'")
    #     print "Successfully connected...."
    # except:
    #     pass

    # cur = conn.cursor()
    flickr = flickrapi.FlickrAPI(api_key, api_secret,format='json')
    # out_file = open("lat_long_train2.txt", 'w')
    # out_file.write("test")
    photoid,_ = literal_eval(record)


    # photoid = '34186307736'
    # photoid = record[0]
    # userid = '62202285@N00'

    try:
        # image_metadata = data_walker(flickr.photos.geo.getLocation,searchstring=,
        #                                 per_page=1000, photo_id= photoid)

        image_metadata = flickr.photos.getInfo(photo_id=photoid,format='json')

        """
            <photo id="32948082713" owner="62202285@N00" secret="1aaa122f05" server="3940" farm="4" title="Fleurs sauvages...!!!" ispublic="1" isfriend="0" isfamily="0" />

        """

        image_metadata = json.loads(image_metadata)
        posted_date = image_metadata['photo']['dates']['posted']
        taken_date = image_metadata['photo']['dates']['taken']

        # print image_metadata['photo']['location']['county']['_content']

        # st = "Insert into image_loc_info2 (photo_id,latitude,longitude,neighbourhood,locality,county,region,country) values "\
        # + "('"+photoid+"',"\
        # +latitude+","\
        # +longitude+",'"\
        # +addslashes(neighbourhood)+"','"\
        # +addslashes(locality)+"','" \
        # + addslashes(county) + "','" \
        # +addslashes(region)+"','"\
        # +addslashes(country)+"')"

        # print st
        tup = (photoid,posted_date,taken_date)
        print tup
        out_file.write(str(tup) + "\n")

        # try:
        #     cur.execute(st)
        # except:
        #     traceback.print_exc()
        #     pass

        # print tup > out_file
    except:
        traceback.print_exc()
        print "Date not found!! ",photoid
        exit(0)


    # conn.close()

def main():
    count = 0



    api_keys = [u'50447f832b7d99785ebb9ba9b69e6a65',u'82764a924643a98e49381f5f28a9a5a7',u'36eadd83335122d888da119424854efc',u'51da9f4ccbd1dae169eb1e619690530e',u'5ebfd342ebab8ea6b16fbbfe6daf632e']
    api_secrets = [u'11d5ef95815b96b0',u'39c68f2dd019d2c0',u'2bbc80b7476185c5',u'5c473c8f547f07d6',u'1e9c1b2440923add']
    # api_key = u'50447f832b7d99785ebb9ba9b69e6a65'
    # api_secret = u'11d5ef95815b96b0'

    import csv
    fil = open('new_photo_ids_train_100.txt', 'r')
    records = fil.readlines()
    # records = records[1:]



    out_file = open('dates_mt_train2.txt','a')
    num_threads = 10
    threads = []
    while count < len(records):
        if threading.active_count() <= num_threads:
            print count
            # print "Number of threads: ",threading.active_count()

            t = threading.Thread(target=get_image_loc,args=(api_keys[count%5],api_secrets[count%5],records[count],out_file))
            threads.append(t)


            t.start()
            # t.join()
            count += 1

    # for x in threads:
    #     x.start()

    # Wait for all of them to finish
    for x in threads:
        x.join()

    out_file.close()

    # get_image_loc(api_keys[count%5],api_secrets[count%5],records)



if __name__ == '__main__':
    main()