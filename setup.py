# -*- coding: utf-8 -*-
"""
This module contains the tool of collective.recipe.omelette
"""
import os
import sys
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


version = "1.1.1"

long_description = (
    "Detailed Documentation\n"
    "**********************\n" + "\n" + read("README.rst") + "\n" + "Change history\n"
    "**************\n" + "\n" + read("CHANGES.txt") + "\n" + "Contributors\n"
    "************\n" + "\n" + read("CONTRIBUTORS.txt")
)
entry_point = "collective.recipe.omelette:Recipe"
uninstall_entry_point = "collective.recipe.omelette:uninstall"

entry_points = {
    "zc.buildout": ["default = %s" % entry_point],
    "zc.buildout.uninstall": ["default = %s" % uninstall_entry_point],
}

install_requires = ["setuptools", "zc.buildout", "zc.recipe.egg"]
tests_require = ["zope.testing", "zc.buildout[test]", "zc.recipe.egg", "pytest"]

if sys.platform[:3].lower() == "win":
    install_requires += ["ntfsutils;python_version<'3.0'"]

setup(
    name="collective.recipe.omelette",
    version=version,
    description="Creates a unified directory structure of installed packages, symlinking to the actual contents, in order to ease navigation.",
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Buildout",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="buildout eggs namespace",
    author="David Glick, Groundwire",
    author_email="davidglick@groundwire.org",
    url="https://github.com/collective/collective.recipe.omelette",
    license="GPL",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["collective", "collective.recipe"],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require=dict(tests=tests_require),
    entry_points=entry_points,
)
