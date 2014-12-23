
def dot(v1, v2):
    N = len(v1)
    s = 0
    for i in xrange(N):
        s += v1[i] * v2[i]
    return s
