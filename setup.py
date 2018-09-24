#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

requirements = [ ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Marcus Kinsella",
    author_email='mkinsella@chanzuckerberg.com',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    description="Tools for working with expression matrices in the HCA Data Coordination Platform",
    install_requires=requirements,
    license="MIT license",
    include_package_data=True,
    keywords='hca_matrix_utils',
    name='hca_matrix_utils',
    packages=find_packages(include=['hca_matrix_utils']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/mckinsel/hca_matrix_utils',
    version='0.0.1',
    zip_safe=False,
)
