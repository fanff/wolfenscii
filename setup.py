# -*- coding: utf-8 -*
from setuptools import find_packages, setup



"""
"""

import sys
import os.path
requirements = []
description=u""

setup(
    name="wolfenscii",
    version="0.1",
    description="Ascii art 3d engine",
    long_description=description,
    author="fanf",
    url="http://github.com/fanff/wolfenscii",
    entry_points={
    },
    install_requires=requirements,
    #test_suite="nose.collector",
    #tests_require=["nose>=1.3", "mock>=1.0", "PyHamcrest>=1.8", "pytest>=2.8"],
    #cmdclass = {
    #    "behave_test": behave_test,
    #},
    extras_require={

    },

    license="BSD",
    classifiers=[
        "Development Status :: 0.0.01.lol",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: Jython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    zip_safe = True,
)


