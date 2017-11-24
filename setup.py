#!/usr/bin/env python

import sys

from setuptools import setup, find_packages

if not sys.version_info[0] == 3:
    print('only python3 supported!')
    sys.exit(1)

setup(
    name='identitySHARK',
    version='0.0.1',
    author='Atefeh Khajeh',
    author_email='atefehkhajeh12@gmail.com',
    description='Merge different developer identities toegether',
    install_requires=[],
    dependency_links=['git+https://github.com/smartshark/pycoSHARK.git@1.0.11#egg=pycoshark-1.0.11'],
    url='https://github.com/smartshark/identitySHARK',
    download_url='https://github.com/smartshark/identitySHARK/zipball/master',
    packages=find_packages(),
    test_suite ='tests',
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache2.0 License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
