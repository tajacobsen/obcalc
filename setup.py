#!/usr/bin/env python

"""
setup.py file for OpenBabel wrapper
"""

"""
To generate swig:
    cd swig
    swig -c++ -python obwrap.i
    mv obwrap.py ../obcalc

To build:
    python setup.py build_ext
"""

from distutils.core import setup, Extension


libraries = [
    'openbabel',
]

library_dirs = [
    '/scratch/s052580/opt/openbabel/lib/',
]

include_dirs = [
    '/usr/include/openbabel-2.0',
    '/scratch/s052580/opt/openbabel/include/openbabel-2.0/',
]

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
