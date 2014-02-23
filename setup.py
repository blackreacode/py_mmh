#!/usr/bin/env python
#! coding: utf-8

import sys 

try:
        from setuptools import setup, Extension
except ImportError:
        from distutils.core import setup, Extension

extra_compile_args = ['-g', '-fPIC', '-Wall', '-O2']

setup(
	name = 'mmh',
	version = '1.0',
	maintainer = 'Michael Lee',
	maintainer_email = 'liyong19861014@gmail.com',
	url = 'https://github.com/airhuman/py_mmh.git',
    	description = 'Python bindings for Google Murmurhash2 hash algorithm',
	ext_modules = [
		Extension('mmh', 
			sources = [
				'mmh.c'
			],
			extra_compile_args = extra_compile_args
		)
	]
)
