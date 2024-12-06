#!/usr/bin/env python3
from setuptools import find_packages, setup

setup(
    name='JsonOperate',
    version='1.0.0',
    description='This wheel is primarily designed for modifying JSON elements.',
    author='ramon Wu',
    author_email='ramon.wu@nokia-sbell.com',
    url='https://gitlab.l1.nsn-net.net/rawu/Json-Operate',
    packages=find_packages(where='src', include=['JsonOperate.*', 'JsonOperate']),
    package_dir = {'':'src'},
    include_package_data=True,
    python_requires='>=3.8.0',
    install_requires=[
        'jsonpath-ng==1.6.0',
    ],
)
