from setuptools import setup, find_packages
import os

with open('README.rst') as f:
    readme = f.read()


def _requires_from_file(filename):
    return open(filename).read().splitlines()


here = os.path.dirname(os.path.abspath(__file__))
version = next((line.split('=')[1].strip().replace("'", '')
                for line in open(os.path.join(here,
                                              '__init__.py'))
                if line.startswith('__version__ = ')),
               '0.0.dev0')

setup(
    name='agatereports',
    version=version[1:-1],
    description='python report generator engine to process JasperReports jrxml file.',
    long_description=readme,
    author='Hitoshi Ozawa',
    author_email='ozawa_h@gmail.com',
    url='https://github.com/ozawa-hi/agatereports',
    # packages=find_packages(exclude=('tests', 'docs', 'demos')),
    packages=find_packages(),
    install_requires=_requires_from_file('requirements.txt'),
    license='BSD license (see LICENSE for details), Copyright (c) 2019, Hitoshi Ozawa',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Office/Business',
        'Topic :: Printing',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.6',
    ],
)
