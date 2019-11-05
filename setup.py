from setuptools import setup

setup(
  name='codb',
  packages=['codb', 'codb.helper'],
  version='1.2.2',
  license='MIT',
  description='common code for DBs',
  long_description=open("README.md").read(),
  long_description_content_type="text/markdown",
  author='Equinox',
  author_email='Alexander.Sales@equinox.com',
  url='https://github.com/equinoxfitness/datacoco.db',
  download_url='https://github.com/equinoxfitness/datacoco.db/archive/v-1.0.tar.gz',
  keywords=['helper', 'common', 'db', 'api'],   # Keywords that define your package best
  install_requires=[
    'psycopg2>=2.8',
    'python-tds==1.9.1',
    'salesforce-bulk==2.1.0',
    'simple-salesforce==0.72.2',
    'salesforce-oauth-request==1.0.6',
    'simplejson==3.14.0',
    'sqlalchemy==1.3.0b1',
    'redis==2.10.6',
    'PyMySQL==0.9.3',
  ]
)
