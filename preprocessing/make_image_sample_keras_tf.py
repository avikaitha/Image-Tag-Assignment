from keras.preprocessing.image import img_to_array, load_img
import numpy as np
from ast import literal_eval
import traceback


def make_image_sample(photo_id_file,image_array_file):
    images_root = "data/images_150X150/"
    x_train = []
    count = 0

    means = None
    stds = None

    with open(photo_id_file,'r') as f:
        train_tups = f.readlines()

    for tup in train_tups:
        id,owner = literal_eval(tup)
        # print id,owner
        file_path = images_root+owner+"/"+id+".jpg"
        # print file_path
        try:
            img_arr = img_to_array(load_img(file_path,target_size=(227,227)))
            for ind in range(img_arr.shape[0]):
                img_arr[ind] = np.fliplr(img_arr[ind])

            if means is None:
                means = [np.mean(img_arr,axis=(0,1))]
                stds = [np.std(img_arr, axis=(0, 1))]
            else:
                means = np.append(means,[np.mean(img_arr,axis=(0,1))],axis=0)
                stds = np.append(stds, [np.std(img_arr, axis=(0, 1))], axis=0)

            x_train.append(img_arr)
            count += 1
            if count % 100 == 0:
                print count

        except:
            # traceback.print_exc()
            pass

    fin_mean = np.mean(means, axis=0)
    fin_stds = np.mean(stds, axis=0)
    fin_x_train = []
    for x in x_train:
        fin_x_train += [(x - fin_mean) / fin_stds]

    fin_x_train = np.array(fin_x_train, dtype=float)

    print fin_x_train.shape
    # print x_train.shape
    # x_train = x_train
    np.save(image_array_file, fin_x_train)

# make_image_sample("new_photo_ids_train_100.txt","image_train_array")
# print "----------------------Validate---------------------------"
# make_image_sample("new_photo_ids_validate_100.txt","image_validate_array")
# print "----------------------Test---------------------------"
# make_image_sample("new_photo_ids_test_100.txt","image_test_array")

# make_image_sample("ids_train.txt","image_train_array")
# print "----------------------Validate---------------------------"
# make_image_sample("ids_validate.txt","image_validate_array")
# print "----------------------Test---------------------------"
# make_image_sample("ids_test.txt","image_test_array")








