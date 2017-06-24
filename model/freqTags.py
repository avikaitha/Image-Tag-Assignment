

import numpy as np
import read_data as readData
import evaluation as eval


def generate_matrix(indx,shape,k):
    
    A = np.zeros((shape[1]))
    for s in xrange(shape[1]):
        for i in xrange(k):
            #print indx[i]
            A[indx[i]] = 1
    
    T = np.zeros(shape)
    for s in xrange(shape[0]):
        T[s,:] = A
        
    return T

path = 'data/dataset/'

print "####################### FreqTag ############################"
print "loading the dataset: please wait for a while!"
X1_train,X2_train,Y_train = readData.read(path+'train/')
X1_test,X2_test,Y_test = readData.read(path+'test/')

file = open('output/FreqTag.txt', 'w')

k = 1
Y_predicted = generate_matrix(np.argsort(np.sum(Y_train,0))[::-1], Y_test.shape, 1)
a, p, r = eval.evaluate(Y_test,Y_predicted,k)
a /= (1. * X1_test.shape[0])
p /= (1. * X1_test.shape[0])
r /= (1. * X1_test.shape[0])
print 'K:1, acc: %.6f, prec: %.6f, rec: %.6f' %(a, p, r)
file.write('K:1, acc: %.6f, prec: %.6f, rec: %.6f' %(a, p, r))
file.write("\n")

k = 3
Y_predicted = generate_matrix(np.argsort(np.sum(Y_train,0))[::-1], Y_test.shape, 1)
a, p, r = eval.evaluate(Y_test,Y_predicted,k)
a /= (1. * X1_test.shape[0])
p /= (1. * X1_test.shape[0])
r /= (1. * X1_test.shape[0])
print 'K:3, acc: %.6f, prec: %.6f, rec: %.6f' %(a, p, r)
file.write('K:1, acc: %.6f, prec: %.6f, rec: %.6f' %(a, p, r))
file.write("\n")

k = 5
Y_predicted = generate_matrix(np.argsort(np.sum(Y_train,0))[::-1], Y_test.shape, 1)
a, p, r = eval.evaluate(Y_test,Y_predicted,k)
a /= (1. * X1_test.shape[0])
p /= (1. * X1_test.shape[0])
r /= (1. * X1_test.shape[0])
print 'K:5, acc: %.6f, prec: %.6f, rec: %.6f' %(a, p, r)
file.write('K:1, acc: %.6f, prec: %.6f, rec: %.6f' %(a, p, r))
file.write("\n")

k = 10
Y_predicted = generate_matrix(np.argsort(np.sum(Y_train,0))[::-1], Y_test.shape, 1)
a, p, r = eval.evaluate(Y_test,Y_predicted,k)
a /= (1. * X1_test.shape[0])
p /= (1. * X1_test.shape[0])
r /= (1. * X1_test.shape[0])
print 'K:10, acc: %.6f, prec: %.6f, rec: %.6f' %(a, p, r)
file.write('K:1, acc: %.6f, prec: %.6f, rec: %.6f' %(a, p, r))
file.close()
