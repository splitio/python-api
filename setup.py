#!/usr/bin/env python

from setuptools import setup, find_packages
from os import path
from sys import version_info

install_requires = [
    'argparse>=1.2.1'
    'colorlog>=2.10.0'
    'requests>=2.14.2'
    'six>=1.10.0'
    'wsgiref>=0.1.2'
]

with open(path.join(path.abspath(path.dirname(__file__)),
                    'splitio', 'version.py')) as f:
    exec(f.read())

setup(
    name='identify_client',
    version=__version__,  # noqa
    description='Split.io Identify Python Client',
    author='Patricio Echague, Sebastian Arrubia, Martin Redolatti',
    author_email='pato@split.io, sebastian@split.io, martin@split.io',
    url='https://github.com/splitio/python-api',
    download_url=(
        'https://github.com/splitio/python-api/tarball/' + __version__
    ),
    license='Apache License 2.0',
    install_requires=install_requires,
    setup_requires=['nose'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
    packages=find_packages()
)
