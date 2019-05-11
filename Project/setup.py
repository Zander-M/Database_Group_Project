# -*- coding: UTF-8 -*- #
# Author: Zander_M
# Time: May, 11, 2019
# Title: Setup File

"""
This is the setup module for the system.
"""

from setuptools import find_packages, setup

setup(
    name="AMS",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe = False,
    install_requires=[
        'flask',
        'werkzeug',
        'pymysql',
        'datetime',
        'click',
        'jinja2',
    ],
)