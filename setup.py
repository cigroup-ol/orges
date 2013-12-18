# -*- coding: utf-8 -*-
"""setup.py script for OrgES."""

from __future__ import division, print_function, with_statement
import os

try:
    from setuptools import setup, find_packages, Extension
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages, Extension
from pip.req import parse_requirements

import orges

HANG_MODULE_EXTENSION = Extension(
    'examples.algorithm.hang',
    sources=['examples/algorithm/hangmodule.c']
)


def extract_package_name(requirement):
    return str(requirement.req).replace('-', '_').split('==')[0]


def find_requirements(req_file='requirements.txt'):
    return [extract_package_name(r) for r in parse_requirements(req_file)]

DESCRIPTION = 'OrgES Package - Organic Computing for Evolution Strategies'
if os.path.isfile('README.rst'):
    long_description = open('README.rst').read()
else:
    long_description = DESCRIPTION

setup(
    author=orges.__author__,
    author_email=orges.__author_email__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Distributed Computing'
    ],
    data_files=[("", ["README.rst", "LICENSE.rst", "requirements_cli.txt",
                      "requirements_examples.txt", "requirements_lint.txt",
                      "requirements_tests.txt"])],
    description=DESCRIPTION,
    ext_modules=[HANG_MODULE_EXTENSION],
    install_requires=[],
    license=orges.__license__,
    name='orges',
    packages=find_packages(exclude=('examples', 'docs', 'tests')),
    package_data={'': ['LICENSE.rst', 'README.rst', 'requirements*.txt']},
    setup_requires='',
    tests_require=find_requirements('requirements_tests.txt'),
    test_suite="tests/",
    url=orges.__url__,
    version=orges.__version__,
)
