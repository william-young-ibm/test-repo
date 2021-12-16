#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='codytest',
    version='0.0.3',
    packages=find_packages(),
    install_requires=[
        'dill==0.3.0',
        'ibm-cos-sdk==2.1.3',
        'numpy==1.18.5',
        'pandas>=0.24.0',
        'scikit-learn==0.23.1',
        'scipy>=1.1.0',
        'requests==2.25.0',
        'urllib3==1.26.3',
        'ibm_db==3.0.2',
        'ibm_db_sa==0.3.5',
        'lxml==4.6.2',
        'nose==1.3.7',
        'psycopg2-binary==2.8.6',
        'pyod==0.7.5',
        'scikit-image==0.16.2',
        'sqlalchemy==1.3.17',
        'tabulate==0.8.5',
        'iotfunctions@git+https://github.com/ibm-watson-iot/functions.git@production'
    ])
