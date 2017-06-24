import numpy as np
from ast import literal_eval

def make_image_tag_vec_mat(user_tag_vec_mat,photo_id_file,image_tag_vec_file):
    user_tag_vec_matrix = np.load(user_tag_vec_mat)

    print user_tag_vec_matrix[0]

    with open(photo_id_file,'r') as f:
        train_tups = f.readlines()

    # try:
    #     conn = psycopg2.connect("dbname='flickr2' user='postgres' host='129.219.60.22' password='password'")
    #     # print "Successfully connected...."
    # except:
    #     pass
    #
    # cur = conn.cursor()

    users = {}
    images = {}
    ind = 0
    ind1 = 0
    for tup in train_tups:
        image_id,owner = literal_eval(tup)
        if owner not in users:
            users[owner] = ind
            ind += 1
            # print ind
        if image_id not in images:
            images[image_id] = ind1
            ind1 += 1


    print len(users)
    print len(images)

    image_tag_word_vec_train = []

    for tup in train_tups:
        image_id,owner = literal_eval(tup)
        image_tag_word_vec_train.append(user_tag_vec_matrix[users[owner]])
        # print users[owner]

    print len(image_tag_word_vec_train[0])
    image_tag_word_vec_train = np.array(image_tag_word_vec_train)
    print image_tag_word_vec_train.shape
    np.save(image_tag_vec_file,image_tag_word_vec_train)


make_image_tag_vec_mat("user_tag_vec_matrix_train.npy","new_photo_ids_train_100.txt","image_tag_word_vec_train")
print "----------------------Validate---------------------------"
make_image_tag_vec_mat("user_tag_vec_matrix_validate.npy","new_photo_ids_validate_100.txt","image_tag_word_vec_validate")
print "----------------------Test---------------------------"
make_image_tag_vec_mat("user_tag_vec_matrix_test.npy","new_photo_ids_test_100.txt","image_tag_word_vec_test")


# make_image_tag_vec_mat("user_tag_vec_matrix_train.npy","ids_train.txt","image_tag_word_vec_train")
# print "----------------------Validate---------------------------"
# make_image_tag_vec_mat("user_tag_vec_matrix_validate.npy","ids_validate.txt","image_tag_word_vec_validate")
# print "----------------------Test---------------------------"
# make_image_tag_vec_mat("user_tag_vec_matrix_test.npy","ids_test.txt","image_tag_word_vec_test")
