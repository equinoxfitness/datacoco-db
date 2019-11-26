from setuptools import setup, find_packages

from codb import VERSION

setup(
    name="codb",
    packages=find_packages(exclude=["tests*"]),
    version=VERSION,
    license="MIT",
    description="common code for DBs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Equinox Fitness",
    url="https://github.com/equinoxfitness/datacoco-db",
    install_requires=[
        "psycopg2-binary>=2.8",
        "python-tds==1.9.1",
        "simplejson==3.14.0",
        "sqlalchemy==1.3.0b1",
        "PyMySQL==0.9.3",
    ],
)
