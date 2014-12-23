from __future__ import print_function
import time
import random

N = 1000000
v1 = [random.random() for i in xrange(N)]
v2 = [random.random() for i in xrange(N)]

def test(module):
    t = time.time()
    ans = module.dot(v1, v2)
    return (ans, time.time() - t)

from cydemo import python_imp
print('python:\t', test(python_imp))

from cydemo import cython_imp
print('cython:\t', test(cython_imp))

from cydemo import cpp_imp
print('cpp:\t', test(cpp_imp))
