import traceback
import numpy as np
from ast import literal_eval

def make_image_user_embeddings(photo_id_file,embedding_file,image_network_embedding_file):
    with open(photo_id_file,'r') as f:
        train_tups = f.readlines()

    users = {}
    ind = 0
    for tup in train_tups:
        image_id,owner = literal_eval(tup)
        if owner not in users:
            users[owner] = ind
            ind += 1
            # print ind

    print len(users)

    with open(embedding_file,'r') as f:
        content = f.readlines()

    content = content[1:]
    user_embeddings = {}
    for row in content:
        temp_list = row.split()
        user_ind = int(temp_list[0])
        temp_list = temp_list[1:]
        embeddings = [float(val) for val in temp_list]
        user_embeddings[user_ind] = embeddings


    print len(user_embeddings)
    image_user_embeddings = []
    for tup in train_tups:
        image_id,owner = literal_eval(tup)

        image_user_embeddings.append(user_embeddings[users[owner]])


    image_user_embeddings = np.array(image_user_embeddings)
    print image_user_embeddings.shape
    np.save(image_network_embedding_file,image_user_embeddings)


# make_image_user_embeddings("new_photo_ids_train_100.txt","train_embeddings.txt","image_user_network_embeddings_train")
# print "----------------------Validate---------------------------"
# make_image_user_embeddings("new_photo_ids_validate_100.txt","validate_embeddings.txt","image_user_network_embeddings_validate")
# print "----------------------Test---------------------------"
# make_image_user_embeddings("new_photo_ids_test_100.txt","test_embeddings.txt","image_user_network_embeddings_test")

# make_image_user_embeddings("ids_train.txt","train_embeddings.txt","image_user_network_embeddings_train")
# print "----------------------Validate---------------------------"
# make_image_user_embeddings("ids_validate.txt","validate_embeddings.txt","image_user_network_embeddings_validate")
# print "----------------------Test---------------------------"
# make_image_user_embeddings("ids_test.txt","test_embeddings.txt","image_user_network_embeddings_test")