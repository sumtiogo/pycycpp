#include "dot.h"

double dot(const std::vector<double> &v1, const std::vector<double> &v2)
{
    int i, N=v1.size();
    double s = 0.0;
    for(i=0; i < N; ++i)
        s = s + v1[i] * v2[i];
    return s;
}
