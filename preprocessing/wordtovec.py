import numpy as np
from gensim import models
from gensim.models.doc2vec import TaggedDocument

def make_user_word2vec_mat(tag_matrix,tag_set,user_tag_vec_mat):
    tag_matrix = np.load(tag_matrix)
    print tag_matrix
    with open(tag_set,'r') as f:
        tags = f.readlines()

    tags = [tag.strip() for tag in tags]
    print len(tags)
    user_tag_vec_matrix = np.empty((tag_matrix.shape[0],128))
    count = 0
    for user_tags in tag_matrix:
        user_tag_list = []
        for ind,_ in enumerate(user_tags):
            if _ > 0:
                user_tag_list += [tags[ind]]*_
        # print user_tag_list
        try:
            sentence = TaggedDocument(words=user_tag_list,tags=["Test"])

            model = models.Doc2Vec([sentence], size=128, window=len(user_tag_list), min_count=1)

            user_tag_vec_matrix[count] = model.docvecs["Test"]
            # print user_tag_vec_matrix[count]
        except:
            user_tag_vec_matrix[count] = np.zeros(128)
            print "Zeross"
            pass
        count += 1
        print count
        # model = models.Word2Vec(user_tag_list,size=len(user_tag_list),window=len(user_tag_list))

        # print model


    print len(user_tag_vec_matrix)
    print user_tag_vec_matrix.shape
    np.save(user_tag_vec_mat,user_tag_vec_matrix)

make_user_word2vec_mat("tag_matrix.npy","tag_set","user_tag_vec_matrix_train")
print "----------------------Validate---------------------------"
make_user_word2vec_mat("tag_matrix_validate.npy","tag_set_validate","user_tag_vec_matrix_validate")
print "----------------------Test---------------------------"
make_user_word2vec_mat("tag_matrix_test.npy","tag_set_test","user_tag_vec_matrix_test")





