#!/usr/bin/env python

from setuptools import setup, find_packages


setup(name='ma_at',
      version='0.0.1',
      description="Shiden Discord Bot",
      author='Andrew Melton',
      author_email='ramielrowe@gmail.com',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'ma_at = ma_at:main',
          ]
      })
