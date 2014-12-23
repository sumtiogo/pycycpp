
def dot(list v1, list v2):
    cdef int i
    cdef int N=len(v1)
    cdef double s = 0;
    for i in xrange(N):
        s = s + v1[i] * v2[i]
    return s
