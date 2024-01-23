#!/usr/bin/env python

import os

from setuptools import setup, find_packages

requirements = []
with open('requirements.txt', 'r') as f:
    for line in f.readlines():
        line = line.strip()
        requirements.append(line)

setup(
    author="Ralph Brecheisen",
    author_email='r.brecheisen@maastrichtuniversity.nl',
    python_requires='>=3.11',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    package_dir={'mosamatic': 'src/app'},
    package=['mosamatic'],
    description="Desktop tool for analyzing medical images",
    install_requires=requirements,
    license="MIT license",
    include_package_data=True,
    keywords='mosamatic',
    name='mosamatic',
    packages=find_packages(),
    setup_requires=requirements,
    entry_points={
        'console_scripts': [
            'mosamatic-desktop=main:main',
        ],
    },
    version=os.environ['VERSION'],
    zip_safe=False,
)