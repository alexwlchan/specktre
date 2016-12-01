#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import codecs
import os

from setuptools import find_packages, setup


def local_file(name):
    return os.path.relpath(os.path.join(os.path.dirname(__file__), name))


SOURCE = local_file('src')
README = local_file('README.rst')
long_description = codecs.open(README, encoding='utf-8').read()

# For PyPI purposes, change the image link to point to GitHub
long_description = long_description.replace(
    'output/demo.png',
    'https://github.com/alexwlchan/specktre/raw/master/output/demo.png')


setup(
    name='specktre',
    version='0.2.0',
    description='A tool for creating wallpapers with Python',
    long_description=long_description,
    url='https://github.com/alexwlchan/specktre',
    author='Alex Chan',
    author_email='alex@alexwlchan.net',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='images wallpaper',
    packages=find_packages(SOURCE),
    package_dir={'': SOURCE},
    install_requires=[
        'docopt',
        'Pillow',
    ],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'specktre=specktre:main',
        ],
    },
)
