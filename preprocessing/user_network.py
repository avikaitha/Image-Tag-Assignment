import psycopg2
import traceback
import numpy as np
from ast import literal_eval
def make_user_network(photo_id_file,edge_list_file):
    with open(photo_id_file,'r') as f:
        train_tups = f.readlines()

    try:
        conn = psycopg2.connect("dbname='flickr2' user='postgres' host='129.219.60.22' password='password'")
        # print "Successfully connected...."
    except:
        pass

    cur = conn.cursor()

    users = {}
    ind = 0
    for tup in train_tups:
        image_id,owner = literal_eval(tup)
        if owner not in users:
            users[owner] = ind
            ind += 1
            # print ind

    print len(users)
    f = open(edge_list_file,'w')
    st = "Select * from fellowship"


    try:
        cur.execute(st)
    except:
        traceback.print_exc()
    while True:
        rows = cur.fetchmany(100000)
        print "Fetched rows"
        if not rows:
            break
        count = 0
        for row in rows:
            try:
                f.write(str(users[row[0]])+" "+str(users[row[1]])+"\n")
                count += 1
            except:
                pass

        print count

make_user_network("new_photo_ids_train_100.txt","train_edge_list.txt")
print "----------------------Validate---------------------------"
make_user_network("new_photo_ids_validate_100.txt","validate_edge_list.txt")
print "----------------------Test---------------------------"
make_user_network("new_photo_ids_test_100.txt","test_edge_list.txt")

# make_user_network("ids_train.txt","train_edge_list.txt")
# print "----------------------Validate---------------------------"
# make_user_network("ids_validate.txt","validate_edge_list.txt")
# print "----------------------Test---------------------------"
# make_user_network("ids_test.txt","test_edge_list.txt")

