from ast import literal_eval
import psycopg2
import traceback
import os


try:
    conn = psycopg2.connect("dbname='flickr2' user='postgres' host='129.219.60.22' password='password'")
    # print "Successfully connected...."
except:
    pass

cur = conn.cursor()
st = "select photo_id,cleaned_tag,owner from image_tags"



tag_set = set()
tag_dict = {}
images_root = "C:\\Users\\akaitha\\PycharmProjects\\flickr_crawler\\images_150X150\\"
try:
    cur.execute(st)
except:
    print "Couldn't execute!!"

while True:
    rows = cur.fetchmany(100000)
    print "Fetched rows"
    if not rows:
        break
    for row in rows:
        photo_id = row[0]
        cleaned_tag = row[1]
        owner = row[2]
        file_path = images_root + owner + "\\" + photo_id + ".jpg"
        if os.path.isfile(file_path):
            if cleaned_tag not in tag_dict:
                tag_dict[cleaned_tag] = 1
            else:
                tag_dict[cleaned_tag] += 1


rem_count = 0
for tag,count in tag_dict.iteritems():
    if count >= 50:
        tag_set.add(tag)
    else:
        rem_count += 1

print len(tag_set)
print rem_count
f = open("global_tag_set",'w')

for tag in tag_set:
    f.write(tag+"\n")

conn.close()





