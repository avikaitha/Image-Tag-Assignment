from ast import literal_eval
import psycopg2
import traceback
import numpy as np

def make_tag_matrix(tag_set_file,photo_id_file,tag_matrix_file):
    with open(tag_set_file,'r') as f:
        tags = f.readlines()


    with open(photo_id_file,'r') as f:
        train_tups = f.readlines()
    try:
        conn = psycopg2.connect("dbname='flickr2' user='postgres' host='129.219.60.22' password='password'")
        # print "Successfully connected...."
    except:
        pass

    cur = conn.cursor()
    # st = "select * from image_tags where photo_id = '"
    st = "select * from image_tags"
    user_tags = {}
    users = {}
    ind = 0
    # tag_set = set()
    for tup in train_tups:
        image_id,owner = literal_eval(tup)
        if owner not in user_tags:
            user_tags[owner] = 0
            users[owner] = ind
            ind += 1
            # print ind




    print len(user_tags),len(tags)

    tag_matrix = [[0]*len(tags) for _ in range(len(users))]

    tag_ind = {}

    ind = 0
    for tag in tags:
        tag_ind[tag.strip()] = ind
        ind += 1
    # print tag_ind
    count = 0
    try:
        cur.execute(st)
    except:
        print "Cannot execute!!"

    while True:
        rows = cur.fetchmany(100000)
        print "Fetched rows"
        if not rows:
            break
        for row in rows:
            try:
                tag_matrix[users[row[2]]][tag_ind[row[4]]] += 1
            except:
                pass



    tag_matrix = np.array(tag_matrix)
    print tag_matrix.shape
    np.save(tag_matrix_file, tag_matrix)
    conn.close()


# make_tag_matrix("tag_set","new_photo_ids_train_100.txt","tag_matrix")
# print "----------------------Validate---------------------------"
# make_tag_matrix("tag_set_validate","new_photo_ids_validate_100.txt","tag_matrix_validate")
# print "----------------------Test-------------------------------"
# make_tag_matrix("tag_set_test","new_photo_ids_test_100.txt","tag_matrix_test")


# make_tag_matrix("tag_set","ids_train.txt","tag_matrix")
# print "----------------------Validate---------------------------"
# make_tag_matrix("tag_set_validate","ids_validate.txt","tag_matrix_validate")
# print "----------------------Test-------------------------------"
# make_tag_matrix("tag_set_test","ids_test.txt","tag_matrix_test")



