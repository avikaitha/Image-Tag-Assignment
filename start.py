from preprocessing.contag.make_context_vector import make_context_vectors
from preprocessing.image_user_embeddings import make_image_user_embeddings
from preprocessing.make_image_sample_keras_tf import make_image_sample

dataset_folder = "data/dataset"
others_folder = "data/others/"


print "----------------------Network Embedding---------------------------"
make_image_user_embeddings(others_folder+"new_photo_ids_train_100.txt",others_folder+"train_embeddings.txt",dataset_folder+"/train/G")
print "----------------------Validate---------------------------"
make_image_user_embeddings(others_folder+"new_photo_ids_validate_100.txt",others_folder+"validate_embeddings.txt",dataset_folder+"/validate/G")
print "----------------------Test---------------------------"
make_image_user_embeddings(others_folder+"new_photo_ids_test_100.txt",others_folder+"test_embeddings.txt",dataset_folder+"/test/G")



print "----------------------Context vectors---------------------------"
make_context_vectors(others_folder+"lat_long_mt_train.txt",others_folder+"dates_mt_train.txt",others_folder+"new_photo_ids_train_100.txt",dataset_folder+"/train/A")
print "----------------------Validate---------------------------"
make_context_vectors(others_folder+"lat_long_mt_validate.txt",others_folder+"dates_mt_validate.txt",others_folder+"new_photo_ids_validate_100.txt",dataset_folder+"/validate/A")
print "----------------------Test---------------------------"
make_context_vectors(others_folder+"lat_long_mt_test.txt",others_folder+"dates_mt_test.txt",others_folder+"new_photo_ids_test_100.txt",dataset_folder+"/test/A")

print "----------------------Image Samples---------------------------"
make_image_sample(others_folder+"new_photo_ids_train_100.txt",dataset_folder+"/train/X")
print "----------------------Validate---------------------------"
make_image_sample(others_folder+"new_photo_ids_validate_100.txt",dataset_folder+"/validate/X")
print "----------------------Test---------------------------"
make_image_sample(others_folder+"new_photo_ids_test_100.txt",dataset_folder+"/test/X")





