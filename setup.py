#!/usr/bin/env python

from setuptools import setup, find_packages

requires = [
    'psycopg2==2.7.7',
    'python-tds==1.9.1',
    'salesforce-bulk==2.1.0',
    'simple-salesforce==0.72.2',
    'salesforce-oauth-request==1.0.6',
    'simplejson==3.14.0',
    'sqlalchemy==1.2.7',
    'redis==2.10.6',
    'PyMySQL==0.9.3',
]

setup(
    name="codb",
    version=1.0,
    author="Equinox",
    description="common code for DBs",
    long_description=open('README.md').read(),
    url="https://bitbucket.org/equinoxfitness/datacoco3.db",
    scripts=[],
    license="TBD",
    packages=find_packages(exclude=["tests*"]),
    install_requires=requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
    dependency_links=[
        "https://github.com/equinoxfitness/datacoco.core#egg=cocore-1.0.0"
    ]
)