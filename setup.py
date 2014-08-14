#coding: utf-8

import os
from setuptools import setup


def read(fn):
    return open(os.path.join(os.path.dirname(__file__), fn)).read()

setup(
    name='django-rest-fias',
    version='0.1.0.0',
    author='Kirov Ilya',
    author_email='kirov@bars-open.ru',
    description=("REST-service for FIAS."),
    license="MIT",
    keywords="django rest fias",
    long_description=read('readme.rst'),
    packages=['django-rest-fias'],
    install_requires=read('requirements'),
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: Russian',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities')
)
