#!/usr/bin/env python3

import glob
import os
import pathlib

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

import numpy

parent_path = pathlib.Path(__file__).parent

# Get numpy include path
numpy_include = numpy.get_include()

numpy_path = os.path.dirname(numpy.__file__)
numpy_include = numpy_path + '/core/include'

CPP_SOURCES = [
    'swig/clustering_wrapper.cpp',
    'swig/SDOstreamclust_wrap.cxx'
]

SDOstreamclust_cpp = Extension(
    'SDOstreamclust.swig._SDOstreamclust',
    CPP_SOURCES,
    include_dirs=['cpp', numpy_include, 'contrib/boost/include'],
    extra_compile_args=['-g0']
)

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='pysdoclust-stream',
    version='0.2',
    license='LGPL-3.0',
    description='SDOstreamclust is an algorithm for clustering data streams',
    author='Simon Konzett',
    author_email='konzett.simon@gmail.com',
    packages=['SDOstreamclust', 'SDOstreamclust.swig'],
    package_dir={'SDOstreamclust': 'python', 'SDOstreamclust.swig': 'swig'},
    ext_modules = [ SDOstreamclust_cpp ],
    install_requires=['numpy'],
    python_requires='>=3.5',
    long_description=description,
    long_description_content_type="text/markdown"
)
