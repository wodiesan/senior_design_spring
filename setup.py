from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import scrying

here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.txt', 'CHANGES.txt')


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='scrying',
    version=scrying.__version__,
    url='https://github.com/wodiesan/senior_design_spring',
    license='The MIT License',
    author='Sze Ron Chau',
    tests_require=['pytest'],
    install_requires=['OpenCV>=3.0',
                      'libavcodec>=56.1.0',
                      'libx264',
                      'libGTK>=2.0-dev',
                      ],
    cmdclass={'test': PyTest},
    author_email='wodiesan@gmail.com',
    description='Computer vision system for the Raspberry Pi 2.',
    long_description=long_description,
    packages=['scrying'],
    include_package_data=True,
    platforms='any',
    test_suite='scrying.test.test_scrying',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Development Status :: 1 - Pre-Alpha',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Education',
        'License :: OSI Approved :: The MIT License',
        'Operating System :: POSIX :: Linux',
        'Topic :: Scientific/Engineering :: Visualization',
        ],
    extras_require={
        'testing': ['pytest'],
    }
)
