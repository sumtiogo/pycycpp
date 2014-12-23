from libcpp.vector cimport vector


cdef extern from 'dot.h':
    double c_dot "dot" (vector[double]& v1, vector[double]& v2)


def dot(list v1, list v2):
    return c_dot(v1, v2)
