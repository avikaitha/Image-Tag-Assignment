from ast import literal_eval
import numpy as np
import datetime



"""

Lat: -90 to 90
Long: -180 to 180

Minute_time: 0 to 1439
Week day: 0-6
Month: 1-12
Day: 1-31

"""
# print image_id,lat,long
def make_context_vectors(lat_long_file,dates_file,photo_id_file,out_file):
    with open(lat_long_file,'r') as f1:
        lat_long = f1.readlines()

    with open(dates_file,'r') as f2:
        dates = f2.readlines()




    image_inds = {}

    ind = 0

    # for date_str in dates:
    #     tup2 = literal_eval(date_str)
    #     image_id = tup2[0]
    #     # print image_id
    #     # break
    #     image_inds[image_id] = ind
    #     ind += 1

    with open(photo_id_file,'r') as f:
        photos = f.readlines()

    for photo in photos:
        tup = literal_eval(photo)
        image_id = tup[0]
        # print image_id
        # break
        image_inds[image_id] = ind
        ind += 1


    print len(image_inds)
    context_vec = np.zeros((len(photos),6))
    for date_str in dates:
        tup2 = literal_eval(date_str)
        image_id = tup2[0]
        posted_date = int(tup2[1])
        date = datetime.datetime.fromtimestamp(posted_date)
        weekday = date.weekday()
        hour = date.hour
        minute = date.minute
        minute_time = hour * 60 + minute
        month = date.month
        day = date.day
        # print date.strftime('%Y-%m-%d %H:%M:%S')
        context_vec[image_inds[image_id]][2] = minute_time
        context_vec[image_inds[image_id]][3] = weekday
        context_vec[image_inds[image_id]][4] = month
        context_vec[image_inds[image_id]][5] = day
        # print (lat, long, weekday, minute_time, month, day)
        # break
        # print posted_date

    for loc_str in lat_long:
        tup1 = literal_eval(loc_str)
        image_id = tup1[0]
        lat = float(tup1[1])
        long = float(tup1[2])
        context_vec[image_inds[image_id]][0] = lat
        context_vec[image_inds[image_id]][1] = long
        print image_inds[image_id]


    print context_vec.shape
    np.save(out_file,context_vec)


# print "----------------------Context vectors---------------------------"
# make_context_vectors("lat_long_mt_train.txt","dates_mt_train.txt","new_photo_ids_train_100.txt","train_A")
# print "----------------------Validate---------------------------"
# make_context_vectors("lat_long_mt_validate.txt","dates_mt_validate.txt","new_photo_ids_validate_100.txt","validate_A")
# print "----------------------Test---------------------------"
# make_context_vectors("lat_long_mt_test.txt","dates_mt_test.txt","new_photo_ids_test_100.txt","test_A")
















