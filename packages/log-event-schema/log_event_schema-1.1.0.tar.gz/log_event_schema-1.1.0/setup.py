# coding: utf-8

from setuptools import setup, find_packages  # noqa: H301

NAME = "log-event-schema"
VERSION = "1.1.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

setup(
    name=NAME,
    version=VERSION,
    description="Lilt Log Event Schema",
    author="AdiFe-code",
    author_email="aditya.sharma@lilt.com",
    url="https://github.com/lilt/log-event-schema",
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    long_description="""\
    Lilt schema to type definition convertor in python for logging events
    """
)
