#!/usr/bin/env python

# Copyright 2011-2012 Eric Wendelin
#
# This is free software, licensed under the Apache License, Version 2.0,
# available in the accompanying LICENSE.txt file.

from setuptools import setup, find_packages

setup(name='lcov_cobertura',
    version='1.6',
    description='LCOV to Cobertura XML converter',
    author='Eric Wendelin',
    author_email='me@eriwen.com',
    url='https://eriwen.github.com/lcov-to-cobertura-xml/',
    download_url='https://raw.githubusercontent.com/eriwen/lcov-to-cobertura-xml/master/lcov_cobertura/lcov_cobertura.py',
    packages=find_packages(),
    package_dir={'': 'lcov_cobertura'},
    provides=['lcov_cobertura'],
    py_modules=['lcov_cobertura'],
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Intended Audience :: Developers',
                 'Natural Language :: English',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 3',
                 'License :: OSI Approved :: Apache Software License',
                 'Topic :: Software Development :: Testing',
                 'Topic :: Software Development :: Quality Assurance'
    ],
    keywords='lcov cobertura',
    install_requires=['lxml'],
    entry_points={
        'console_scripts': ['lcov_cobertura=lcov_cobertura:main']
    },
    license='Apache License, Version 2.0'
)
