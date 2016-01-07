# -*- coding: utf-8 -*-
"""
    setup.py
    ~~~~~~~~

    Setup script for fileserver

    :copyright: (c) 2015 by Saeed Abdullah.
"""

from setuptools import setup

setup(
    name="fileserver",
    version="0.1",
    long_description=__doc__,
    packages=["fileserver"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "Flask==0.10.1",
    ],
)
