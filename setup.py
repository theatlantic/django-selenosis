#!/usr/bin/env python
import io
from os import path

from setuptools import setup, find_packages


def read(*parts):
    file_path = path.join(path.dirname(__file__), *parts)
    return io.open(file_path).read()


setup(
    name='django-selenosis',
    version='1.3.0',
    license='BSD',
    description='Helpers for writing selenium tests for Django',
    long_description=read('README.rst'),
    url='https://github.com/theatlantic/django-selenosis',
    author='Frankie Dintino',
    author_email='fdintino@theatlantic.com',
    maintainer='Frankie Dintino',
    maintainer_email='fdintino@theatlantic.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django>=1.11',
        'six',
    ],
    entry_points={
        "pytest11": [
            "selenosis = selenosis.pytest_plugin.selenosis",
            "tags = selenosis.pytest_plugin.tags",
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ])
