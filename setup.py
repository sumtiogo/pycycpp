from distutils.core import setup, Extension
from Cython.Distutils import build_ext

ext_modules = []

ext_modules.append(
    Extension(
        # output module path
        'cydemo.cython_imp',
        # source pyx module
        ['cydemo/cython_imp.pyx']
    )
)


setup(
    name='CyDemo',
    packages=['cydemo'],
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules,
)
