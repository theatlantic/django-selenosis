#!/usr/bin/env python
import io
from os import path

from setuptools import setup, find_packages


def read(*parts):
    file_path = path.join(path.dirname(__file__), *parts)
    return io.open(file_path).read()


setup(
    name='django-selenosis',
    version='1.4.0',
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
    python_requires=">=3.6",
    install_requires=[
        'Django>=2.2',
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ])
