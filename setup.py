# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='leven-squash',
    version='0.0.1',
    description='Method for very fast Levenstein distance approximation',
    long_description=readme,
    author='Dodge W. Coates',
    author_email='dodge.w.coates@gmail.com',
    url='NONE',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)