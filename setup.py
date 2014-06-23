#!/usr/bin/env python

from setuptools import setup, find_packages

#one line description
with open('DESCRIPTION') as F:
    description = F.read().strip()

#version number
with open('VERSION') as F:
    version = F.read().strip()


setup(name='ruru',
      version=version,
      description=description,
      author='Mark Fiers',
      author_email='mark.fiers.42@gmail.com',
      include_package_data=True,
      url='https://encrypted.google.com/#q=ruru&safe=off',
      packages=find_packages(),
      install_requires=[
                'matplotlib',
                ],
      classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        ]
     )
