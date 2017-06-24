

import numpy as np

def read(path):
    X1 = np.load(path+'X.npy').astype('float32')
    X2 = np.load(path+'G.npy').astype('float32')
    Y = np.load(path+'Y.npy').astype('float32')
    return X1,X2,Y
    
def readCoTagNet(path):
    return np.load(path+'A.npy').astype('float32')
