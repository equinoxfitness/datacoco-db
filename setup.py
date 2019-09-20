from distutils.core import setup

setup(
  name='codb',
  packages=['codb'],
  version=1.0,
  license='MIT',
  description='common code for DBs',
  author='Equinox',
  author_email='n/a',
  url='https://github.com/equinoxfitness/datacoco.db',
  download_url='https://github.com/equinoxfitness/datacoco.db/archive/v-1.0.tar.gz',
  keywords=['helper', 'common', 'db', 'api'],   # Keywords that define your package best
  install_requires=[
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
)
