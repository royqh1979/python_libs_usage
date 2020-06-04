import numpy as np
from timeit import timeit
from sortedcontainers import SortedList,SortedDict
from bintrees import FastAVLTree

lst =np.random.uniform(size=10000000)

sl = SortedDict()
def insert_sl():
    global sl
    sl = SortedDict()
    for v in lst:
        sl[v]=None

tree= FastAVLTree()
def insert_tree():
    global tree
    tree = FastAVLTree()
    for v in lst:
        tree.insert(v,None)

def find_sl():
    for v in lst:
        p=sl.get(v)

def find_tree():
    for v in lst:
        tree.get_value(v)

print(timeit(insert_sl,number=10))
print(timeit(insert_tree,number=10))
print(timeit(find_sl,number=10))
print(timeit(find_tree,number=10))
