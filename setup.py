#!/usr/bin/env python
from os import path
import re

from setuptools import setup, find_packages


# Find the package version in __init__.py without importing it
init_file = path.join(path.dirname(__file__), "selenosis", "__init__.py")
with open(init_file) as f:
    for line in f:
        m = re.search(r"""^__version__ = (['"])(.+?)\1$""", line)
        if m is not None:
            version = m.group(2)
            break
    else:
        raise LookupError("Unable to find __version__ in " + init_file)



def read(*parts):
    file_path = path.join(path.dirname(__file__), *parts)
    return open(file_path).read()


setup(
    name='django-selenosis',
    version=version,
    license='BSD',
    description='Helpers for writing selenium tests for Django',
    long_description=read('README.rst'),
    url='https://github.com/theatlantic/django-selenosis',
    author='Frankie Dintino',
    author_email='fdintino@theatlantic.com',
    maintainer='Frankie Dintino',
    maintainer_email='fdintino@theatlantic.com',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=['Django>=2.2',],
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
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ])
