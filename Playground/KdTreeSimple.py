#
#simple demo of sklearn's  kdtree 
#https://stackoverflow.com/questions/48126771/nearest-neighbour-search-kdtree
#
import numpy as np
from sklearn.neighbors import KDTree
np.random.seed(0)
X = np.random.random((5, 2))  # 5 points in 2 dimensions
tree = KDTree(X)
nearest_dist, nearest_ind = tree.query(X, k=2)  # k=2 nearest neighbors where k1 = identity
print(X)
print(nearest_dist[:, 1])    # drop id; assumes sorted -> see args!
print(nearest_ind[:, 1])     # drop id 


#How does Kdtree work?
'''
    Begin with a n dimensional numpy array. This is an array of n dimensional vector (X)
    Pass X into constructor of tree=KDtree()
    The 'query' method produces a 2 results
        nearest_dist    ->  an array of shortest distance. 1 element per item in X. Each item gives the distance to the nearest vector
        nearest_ind     ->  an array of indices. Every element stores the index to the vector in X which is nearest to the element
'''
