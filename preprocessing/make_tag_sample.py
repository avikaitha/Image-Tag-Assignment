from ast import literal_eval
import psycopg2
import traceback

def make_tag_sets(photo_id_file,tag_set_file):
    with open(photo_id_file,'r') as f:
        train_tups = f.readlines()
    try:
        conn = psycopg2.connect("dbname='flickr2' user='postgres' host='129.219.60.22' password='password'")
        # print "Successfully connected...."
    except:
        pass

    cur = conn.cursor()
    st = "select photo_id,cleaned_tag from image_tags"

    photoids = set()

    for tup in train_tups:
        image_id, owner = literal_eval(tup)
        photoids.add(image_id)

    print len(photoids)

    tag_set = set()
    tag_dict = {}

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

            if photo_id in photoids:
                if cleaned_tag not in tag_dict:
                    tag_dict[cleaned_tag] = 1
                else:
                    tag_dict[cleaned_tag] += 1


    rem_count = 0
    tag_count = 0
    for tag,count in tag_dict.iteritems():
        if count >= 50:
            tag_count += count
            tag_set.add(tag)
        else:
            rem_count += 1

    print tag_count
    print len(tag_set)
    print rem_count
    f = open(tag_set_file,'w')

    for tag in tag_set:
        f.write(tag+"\n")

    conn.close()


make_tag_sets("new_photo_ids_train_100.txt","tag_set2")
print "----------------------Validate---------------------------"
make_tag_sets("new_photo_ids_validate_100.txt","tag_set_validate2")
print "----------------------Test---------------------------"
make_tag_sets("new_photo_ids_test_100.txt","tag_set_test2")

# make_tag_sets("ids_train.txt","tag_set")
# print "----------------------Validate---------------------------"
# make_tag_sets("ids_validate.txt","tag_set_validate")
# print "----------------------Test---------------------------"
# make_tag_sets("ids_test.txt","tag_set_test")



