#!/usr/bin/env python

from setuptools import setup, find_packages

requirements = [
    'cryptography>=2.8',
    'requests-oauthlib>=1.2',
    'tornado>=6.0.3',
    'jupyterhub-kubespawner>=0.11'
]

with open('README.md') as rm:
    long_description = rm.read()

setup(
    name='kujudrivespawner',
    version='0.1.1',
    description='Utilities to integrate seadrive with KubeSpawner',
    long_description=long_description,
    author='Human Brain Project Collaboratory Team',
    author_email='support@humanbrainproject.eu',
    url='https://wiki.humanbrainproject.eu/',
    packages=find_packages(),
    install_requires=requirements
)
