# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='agatereports',
    version='0.1.0',
    description='python generator for jrxml file.',
    long_description=readme,
    author='Hitoshi Ozawa',
    author_email='ozawa_h@gmail.com',
    url='https://github.com/ozawa-hi/agatereports',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
