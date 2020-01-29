import os
import re
from setuptools import setup, find_packages


def get_version():
    version_file = open(os.path.join("datacoco_db", "__version__.py"))
    version_contents = version_file.read()
    return re.search('__version__ = "(.*?)"', version_contents).group(1)


setup(
    name="datacoco-db",
    packages=find_packages(exclude=["tests*"]),
    version=get_version(),
    license="MIT",
    description="Data common code for database interactions by Equinox",
    long_description=open("README.rst").read(),
    author="Equinox Fitness",
    url="https://github.com/equinoxfitness/datacoco-db",
    install_requires=[
        "psycopg2-binary>=2.8",
        "pyodbc==4.0.28",
        "python-tds==1.9.1",
        "simplejson==3.14.0",
        "sqlalchemy==1.3.0b1",
        "PyMySQL==0.9.3",
        "jsonschema==3.2.0",
    ],
)
