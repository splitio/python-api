#!/usr/bin/env python

import subprocess
import contextlib
import sys
import pkg_resources
from setuptools import setup, find_packages
from os import path
from distutils.cmd import Command
from pathlib import Path

@contextlib.contextmanager
def _save_argv(repl=None):
    saved = sys.argv[:]
    if repl is not None:
        sys.argv[:] = repl
    try:
        yield saved
    finally:
        sys.argv[:] = saved


class E2ETests(Command):
    '''
    Custom command to run End to End tests with locally mocked
    tornado webserver.
    '''
    description = 'Run end to end tests with mocked tornado backend'
    user_options = [
        ('addopts=', None, "Additional options to be passed verbatim to the "
         'pytest runner')
    ]

    def initialize_options(self):
        '''
        '''
        self.addopts = []

    def finalize_options(self):
        '''
        '''
        pass

    def _setup_tornado(self):
        '''
        '''
        try:
            import tornado
        except ImportError:
            subprocess.check_call(['pip', 'install'] + locale2e_requires)

    def _setup_pytest(self):
        '''
        '''
        current_dir = path.dirname(path.realpath(__file__))
        egg_path = path.join(current_dir, '.eggs')
        pkg_resources.working_set.add_entry(egg_path)
        pkg_resources.require('pytest')

    def _setup_args(self):
        '''
        '''
        le2e_test_file = path.join(
            path.dirname(path.realpath(__file__)),
            'splitapiclient',
            'tests',
            'e2e',
            'e2etests.py'
        )
        return ['pytest', '-v'] + [le2e_test_file] + self.addopts

    def run(self):
        '''
        '''
        self._setup_tornado()
        self._setup_pytest()
        import pytest
        with _save_argv(self._setup_args()):
            __import__('pytest').main()

# Project requirements
install_requires = [
    'argparse>=1.1',
    'requests>=2.14.2',
    'six>=1.10.0',
]


# Standard unit test requirements
tests_requires = [
    'mock==2.0.0',
    'pytest-mock==1.6.0',
    'pytest==6.2.4',
]


# Local End to End test requirements
locale2e_requires = [
    'tornado'
]


# Get version number
with open(path.join(path.abspath(path.dirname(__file__)),
                    'splitapiclient', 'version.py')) as f:
    exec(f.read())
# Run setup!
this_directory = Path(__file__).parent
setup(
    name='splitapiclient',
    version=__version__,  # noqa
    description='This Python Library provide full support for Split REST Admin API',
    long_description=(this_directory / "README.md").read_text(),
    long_description_content_type='text/markdown',
    author='Patricio Echague, Sebastian Arrubia, Martin Redolatti',
    author_email='pato@split.io, sebastian@split.io, martin@split.io',
    url='https://github.com/splitio/python-api',
    download_url=(
        'https://github.com/splitio/python-api/tarball/' + __version__
    ),
    license='Apache License 2.0',
    install_requires=install_requires,
    setup_requires=['pytest-runner'],
    tests_require=tests_requires,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
    packages=find_packages(),
    cmdclass={
        'e2etests': E2ETests,
    }
)
