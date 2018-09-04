#!/usr/bin/env python

from os.path import abspath, dirname, join
from setuptools import setup, find_packages
from sys import path

path.append(abspath(join(dirname(__file__), 'src')))

from python_exercice import __VERSION__

# Installation Dependencies
install_dependencies = [
    'Django >= 2.1, < 2.2',
    'django-extensions >= 2.1, < 2.2',
    'mysqlclient == 1.3.13',
    'requests == 2.19.1',
    'redis == 2.10.6',
    'celery == 4.2.1',
    'raven >= 6, < 7',
    'jsonschema >= 2.6.0',
    'factory_boy == 2.11.1',
    'safety',
]

setup(
    name='python_exercice',
    version=__VERSION__,
    author='Yohan Lebret',
    author_email='yohan.lebret@gmail.com',
    description='',
    zip_safe=False,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=install_dependencies,
    include_package_data=True,
    classifiers=[
        'Environment :: Console',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)