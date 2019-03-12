# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

def _requires_from_file(filename):
    return open(filename).read().splitlines()

# version
here = os.path.dirname(os.path.abspath(__file__))
version = next((line.split('=')[1].strip().replace("'", '')
                for line in open(os.path.join(here,
                                              'agatereports',
                                              '__init__.py'))
                if line.startswith('__version__ = ')),
               '0.0.dev0')

setup(
    name='agatereports',
    version='0.1.0',
    description='python report generator engine using JasperReports jrxml file.',
    long_description=readme,
    author='Hitoshi Ozawa',
    author_email='ozawa_h@gmail.com',
    url='https://github.com/ozawa-hi/agatereports',
    license=license,
    packages=find_packages(exclude=('tests', 'docs', 'demos'))
    install_requires=_requires_from_file('requirements.txt'),
    license="BSD license (see LICENSE for details), Copyright (c) 2019, Hitoshi Ozawa",
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Printing',
        'Topic :: Text Processing :: Markup',
        'Programming Language :: Python :: 3.6',
    ],
)
