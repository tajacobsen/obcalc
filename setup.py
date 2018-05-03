#!/usr/bin/env python

"""
setup.py file for obcalc
"""

"""
To generate swig files:
    cd swig
    swig -c++ -python obwrap.i
    mv obwrap.py ../obcalc

    Note: when using python3 one has to use
    swig -c++ -py3 obwrap.i


To build:
    python setup.py build_ext
"""

from distutils.core import setup, Extension
import os


libraries = [
    'openbabel',
]
library_dirs = []
include_dirs = []

customize = 'customize.py'
if os.path.isfile(customize):
    # workaround for execfile that work
    # python2 and python3
    exec(compile(open(customize).read(), customize, 'exec'))

obwrap_module = Extension('_obwrap',
                          sources=['swig/obwrap_wrap.cxx', 'swig/obwrap.cxx'],
                          libraries=libraries,
                          library_dirs=library_dirs,
                          include_dirs=include_dirs,
                         )

py_modules = [
    'obcalc/__init__',
    'obcalc/tools',
    'obcalc/obwrap',
]

setup (name = 'obcalc',
       version = '0.1',
       author      = "Troels Kofoed Jacobsen",
       description = """An OpenBabel calculator implementing the standard ASE interface""",
       ext_modules = [obwrap_module],
       py_modules = py_modules,
       )
