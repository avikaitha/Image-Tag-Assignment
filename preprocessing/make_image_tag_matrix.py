from ast import literal_eval
import psycopg2
import numpy as np
import traceback

def make_image_tag_matrix(photo_id_file,image_tag_file):
    try:
        conn = psycopg2.connect("dbname='flickr2' user='postgres' host='129.219.60.22' password='password'")
        # print "Successfully connected...."
    except:
        pass

    cur = conn.cursor()
    st = "select * from image_tags"

    with open("tag_set",'r') as f:
        tags = f.readlines()

    tags = [tag.strip() for tag in tags]

    tag_ind = {}
    ind = 0
    for tag in tags:
        if tag not in tag_ind:
            tag_ind[tag] = ind
            ind += 1

    print tag_ind

    with open(photo_id_file,'r') as f:
        train_tups = f.readlines()

    image_tag_matrix = np.zeros((len(train_tups),len(tag_ind)),dtype=int)


    ind = 0
    img_ind = {}
    for tup in train_tups:
        image_id,owner = literal_eval(tup)
        img_ind[image_id] = ind
        ind += 1

    #print img_ind

    try:
        cur.execute(st)
    except:
        pass

    while True:
        rows = cur.fetchmany(100000)
        print "Fetched rows"
        if not rows:
            break
        for row in rows:
            tag = row[4]
            try:
                image_tag_matrix[img_ind[row[1]]][tag_ind[tag]] = 1
                print row[1],tag, [tag_ind[tag]]
            except:
                #traceback.print_exc()
                pass

    print image_tag_matrix.shape
    print np.sum(image_tag_matrix)
    np.save(image_tag_file,np.array(image_tag_matrix))

    conn.close()

# make_image_tag_matrix("new_photo_ids_train_100.txt","image_tags_train")
# print "----------------------Validate---------------------------"
# make_image_tag_matrix("new_photo_ids_validate_100.txt","image_tags_validate")
print "----------------------Test---------------------------"
make_image_tag_matrix("new_photo_ids_test_100.txt","image_tags_test")


# make_image_tag_matrix("ids_train.txt","image_tags_train")
# print "----------------------Validate---------------------------"
# make_image_tag_matrix("ids_validate.txt","image_tags_validate")
# print "----------------------Test---------------------------"
# make_image_tag_matrix("ids_test.txt","image_tags_test")



