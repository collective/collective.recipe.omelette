"""
This module contains the tool of collective.recipe.omelette
"""

from setuptools import find_packages
from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


version = "2.0.1.dev0"

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
tests_require = ["zope.testing", "zc.buildout[test]", "zc.recipe.egg"]

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
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    keywords="buildout eggs namespace",
    author="David Glick, Groundwire",
    author_email="davidglick@groundwire.org",
    url="https://github.com/collective/collective.recipe.omelette",
    license="GPL",
    packages=find_packages(),
    namespace_packages=["collective", "collective.recipe"],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    python_requires=">=3.9",
    extras_require=dict(
        test=tests_require,
        # Originally we only had 'tests' as entrypoint,
        # but we prefer 'test'.
        tests=tests_require,
    ),
    entry_points=entry_points,
)
