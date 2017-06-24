import psycopg2
import numpy as np
import traceback
import os.path
import operator





NUM_PHOTOS_PER_USER = 100
# NUM_PHOTOS = 2173505
import csv
usr_ids = []
with open("new_usrid_full.txt",'r') as f:
    # content = csv.reader(f)
    content = f.readlines()
    count = 0
    for row in content:
        # print row
        usr_ids += [row.strip()]
        # usr_ids += [row[0]]
        count += 1

# usr_ids = usr_ids[1:]
print len(usr_ids)

# usr_photos = {}
usr_id_dict = {}
usr_photos_tags = {}

ind = 0
for usr_id in usr_ids:
    # usr_photos[usr_id] = []
    usr_id_dict[usr_id] = ind
    usr_photos_tags[usr_id] = {}
    ind += 1

with open("global_tag_set",'r') as f:
    tag_set = f.readlines()

tag_set = [tag.strip() for tag in tag_set]

tag_set = set(tag_set)

print len(tag_set)
# tag_set = {}

try:
    conn = psycopg2.connect("dbname='flickr2' user='postgres' host='129.219.60.22' password='password'")
    # print "Successfully connected...."
except:
    pass

cur = conn.cursor()

st = 'select photo_id,owner,cleaned_tag from image_tags'

try:
    cur.execute(st)
except:
    print "Couldn't execute!!"
images_root = "C:\\Users\\akaitha\\PycharmProjects\\flickr_crawler\\images_150X150\\"

flags = [0]*len(usr_ids)
out1 = open("new_photo_ids_train_100.txt",'w')
out2 = open("new_photo_ids_validate_100.txt",'w')
out3 = open("new_photo_ids_test_100.txt",'w')
photo_set = set()
fetched_count = 0
while True:
    # print "Users Done:",sum(flags)
    if sum(flags) == len(usr_ids):
        break

    rows = cur.fetchmany(100000)
    print "Fetched rows",fetched_count
    if not rows:
        break
    for row in rows:
        photo_id = row[0]
        owner = row[1]
        cleaned_tag = row[2]
        try:
            # if len(usr_photos[owner]) < NUM_PHOTOS_PER_USER:
            file_path = images_root + owner + "\\" + photo_id + ".jpg"
            if os.path.isfile(file_path):
                if cleaned_tag in tag_set:
                    if photo_id not in photo_set:
                        # usr_photos[owner] += [(photo_id,owner)]
                        usr_photos_tags[owner][photo_id] = 1
                        photo_set.add(photo_id)
                        # if cleaned_tag not in tag_set:
                        #     tag_set[cleaned_tag] = 1
                        # else:
                        #     tag_set[cleaned_tag] += 1

                    else:
                        usr_photos_tags[owner][photo_id] += 1
        except:
            # traceback.print_exc()
            pass

    # print len(usr_photos_tags[owner])
    fetched_count += 1

for owner in usr_ids:
    photo_dict = usr_photos_tags[owner]
    if len(photo_dict) > NUM_PHOTOS_PER_USER:
        photo_dict = dict(sorted(photo_dict.items(), key=operator.itemgetter(1))[-100:])



    photo_ids = list(photo_dict.keys())
    # print len(photo_ids), owner
    count = 0

    if flags[usr_id_dict[owner]] != 1:
        for photo_id in photo_ids:
            if count < int(.8 * NUM_PHOTOS_PER_USER):
                # print "This",str((photo_id, owner))
                out1.write(str((photo_id, owner)) + "\n")
            elif count < int(.90 * NUM_PHOTOS_PER_USER):
                out2.write(str((photo_id, owner)) + "\n")
            elif count < int(NUM_PHOTOS_PER_USER):
                out3.write(str((photo_id, owner)) + "\n")
            if count == NUM_PHOTOS_PER_USER-1:
                flags[usr_id_dict[owner]] = 1
            count += 1

out1.close()
out2.close()
out3.close()

count = 0
for ind,flag in enumerate(flags):
    if flag == 0:
        print '"'+usr_ids[ind]+'",'
        count += 1
print count
# count = 0
# f = open("new_usrid_full.txt",'w')
# for ind,flag in enumerate(flags):
#     if flag == 1:
#         print '"'+usr_ids[ind]+'",'
#         f.write(usr_ids[ind]+"\n")
#         count += 1
#
# print count






