#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='nameko-atomicity',
    version='1.0.0',
    description='Atomicity dependency for nameko services',
    author='jeremy-jin',
    author_email='306795597@qq.com',
    url='https://github.com/jeremy-jin/nameko-atomicity',
    packages=find_packages(exclude=("test",)),
    install_requires=[
        "nameko>=2.0.0",
    ],
    extras_require={
        'dev': [
            "coverage==5.5",
            "flake8==3.9.2",
            "pylint==2.8.3",
            "pytest==6.2.4",
            "black==21.5b2"
        ]
    },
    zip_safe=True,
    license='Apache License, Version 2.0',
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)