import numpy as np


def evaluate_k(gt, est, k=5):
    """
        the est are the estimated labels
        """
    n_tags = gt.shape[0]
    tp_ptag = np.zeros(n_tags)
    ap_ptag = np.zeros(n_tags)
    total_ptag = np.zeros(n_tags)

    acc = 0.0
    prec = 0.0
    rec = 0.0
    tp = 0.0

    tag_ids = est.argsort()[::-1]

    for i in range(k):
        _id = tag_ids[i]
        if gt[_id] == 1:
            acc = 1.0
            tp += 1.0
    
    
    prec = tp/(1. *k)
    if np.sum(gt)==0:
        rec = 0
    else:
        rec = tp/(1. *np.sum(gt))

    if k == 5:
        #print tp," -> ",tag_ids[0:5]
        num_tags = np.sum(gt)
        for i in range(num_tags):
            _id = tag_ids[i]
            ap_ptag[_id] += 1
            if gt[_id] == 1:
                tp_ptag[_id] += 1
            
        total_ptag += gt

    return acc, prec, rec

def evaluate(labels, predicteds, k=5):
    
    num_asamples = labels.shape[0]
    acc = 0.0
    prec = 0.0
    rec = 0.0
    for i in xrange(num_asamples):
        a, p, r = evaluate_k(labels[i],predicteds[i],k)
        acc += a
        prec += p
        rec += r
    
    #acc /= (1. * num_asamples)
    #prec /= (1. * num_asamples)
    #rec /= (1. * num_asamples)
    
    #print 'acc: %.6f, prec: %.6f, rec: %.6f' %(acc, prec, rec)
    return acc, prec, rec
    
