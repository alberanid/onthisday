#!/usr/bin/env python3

from distutils.core import setup

setup(name='onthisday',
      version='1.0',
      description='What REALLY happened in the world, on this day.',
      author='Davide Alberani',
      author_email='da@mimante.net',
      license='Apache 2.0',
      url='https://github.com/alberanid/onthisday/',
      py_modules=['onthisday'],
      requires=['markovify'])
