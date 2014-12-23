CyDemo
==========

This is a simple demo about cython.

I will write 3 kinds of implementation of inner product:

1. python
2. cython
3. c code with cython as wrapper

and write a test script to measure their excution time.

Let's go!

## Step 0 - Environment

I develop my project on dockerfile/python

    docker run -it --rm dockerfile/python

and install cython by pip

    pip install cython
  
But you could absolutely develop it without docker; just make sure you install cython for your python

## Step 1 - Python

Please checkout to step-1

    git checkout step-1
  
In this step, we write a simple python code

```python
def dot(v1, v2):
    N = len(v1)
    s = 0
    for i in xrange(N):
    ¦   s += v1[i] * v2[i]
    return s
```

also, put it in `cydemo` folder and create a empty `__init__.py` file, so we have a beautiful and standard python package structure.

```
└── cydemo
    ├── __init__.py
    └── python_imp.py
```

## Step 2 - Cython

Please checkout to step-2
    
    git checkout step-2

The project structure become

```
├── cydemo
│   ├── __init__.py
│   ├── cython_imp.pyx
│   └── python_imp.py
└── setup.py
```

In this step, we get two more file, let's take a look on `cydemo/cython_imp.pyx`

```cython
def dot(list v1, list v2):
    cdef int i
    cdef int N=len(v1)
    cdef double s = 0;
    for i in xrange(N):
    ¦   s = s + v1[i] * v2[i]
    return s
```

something noticiable:

- the syntax is pretty like python. for more, check [cython doc](http://docs.cython.org/)
- the file extension of cython is `.pyx`

different from python code, cython code need compilation before excution, so we write `setup.py` to help us.

```python
from distutils.core import setup
from distutils import Extension
from Cython.Distutils import build_ext

ext_modules = []

ext_modules.append(
    Extension(
    ¦   # output module path
    ¦   'cydemo.cython_imp',
    ¦   # source pyx module
    ¦   ['cydemo/cython_imp.pyx']
    )
)

setup(
    name='CyDemo',
    packages=['cydemo'],
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules,
)
```

- we tell setup function to use cython.build_ext to build the cython code for us
- we declare a extension `cydemo.cython_imp` and specify it should be compiled from `cydemo/cython_imp.pyx`

later when we run `setup.py`, it will complie our cython code and create a 'cydemo/cython_imp.so' for us; with that file,
we could import that module as it is a standard python module.

## Step 3 - C code with cython wrapper

checkout step-3

    git checkout step-3
    
The project structure become

```
├── cydemo
│   ├── __init__.py
│   ├── cpp_imp_wrapper.pyx
│   ├── cython_imp.pyx
│   └── python_imp.py
├── extension
│   ├── include
│   │   └── dot.h
│   └── lib
│       └── dot.cpp
└── setup.py
```

This step is slightly complex, let's start from the extension folder.

```cpp
// extension/include/dot.h
#include <vector>                                                               

double dot(const std::vector<double> &v1, const std::vector<double> &v2);
```

```cpp
// extension/lib/dot.cpp
#include "dot.h"

double dot(const std::vector<double> &v1, const std::vector<double> &v2)
{
    int i, N=v1.size();
    double s = 0.0;
    for(i=0; i < N; ++i)
    ¦   s = s + v1[i] * v2[i];
    return s;
}
```

Here we write a simple cpp version inner production function.
Then we write a cyhton wrapper to bridge the C world and Python world well. :)

```cython
# cydemo/cpp_imp_wrapper.pyx
from libcpp.vector cimport vector                                               


cdef extern from 'dot.h':
    double c_dot "dot" (vector[double]& v1, vector[double]& v2)


def dot(list v1, list v2):
    return c_dot(v1, v2)
```

Notice that we alias the function name `dot` to `c_dot` here. This is not necessary unless you want to use the same name as python function. You may checkout the [cython doc](http://docs.cython.org/src/userguide/external_C_code.html#resolving-naming-conflicts-c-name-specifications) for more info.

Now it's time to checkout the modification of `setup.py`. We only declare one more extension.

```python
# some previous code in step-2 ...

ext_modules.append(
    Extension(
    ¦   'cydemo.cpp_imp',
    ¦   sources=[                                                               
    ¦   ¦   'cydemo/cpp_imp_wrapper.pyx',
    ¦   ¦   'extension/lib/dot.cpp'],
    ¦   include_dirs=['extension/include'],
    ¦   language='c++'
    )
)

# some previous code in step-2 ...

```

After compilation, there will be a `cydemo/cpp_imp.so` file, and it will be complied from the `sources`. When compiling c code,
`-I` flag will include the `include_dirs`, and since the `language` is `c++`, so it will use `g++` or any other compitiable compiler. Everything is so explicit, thanks the syntax of python!

## step-4 - Test

Checkout step-4

    git checkout step-4
    
```
├── cydemo
│   ├── __init__.py
│   ├── cpp_imp_wrapper.pyx
│   ├── cython_imp.pyx
│   └── python_imp.py
├── extension
│   ├── include
│   │   └── dot.h
│   └── lib
│       └── dot.cpp
├── setup.py
└── tests
    └── main.py
```

We only got one more file in this step `tests/main.py`

```python
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
```

In this python code, we randomly generate two vector, and measure the elapsed time for different implementation.

Before test, you should install this whole package

    python setup.py install
    
the build procedure is quite interesting, you could observe it generating the `.so` file, the `-I` flag, and where it put as we mention before. Take a look!

In the end, we run `main.py`

    python tests/main.py
    
and here is the output

```
python:  (250078.6439168099, 0.1044008731842041)
cython:  (250078.6439168099, 0.05468893051147461)
cpp:     (250078.6439168099, 0.0352931022644043)

# the hidden boss, which not cover in this tutorial
pypy:    (250312.47666717478, 0.004452943801879883)
```

And once again, the day is end .Thank you, the Powerpuff girls！

## TODO

- [Parallelism](http://docs.cython.org/src/userguide/parallelism.html)
