# -*- coding: utf-8 -*-
"""
This module contains the tool of collective.recipe.omelette
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.7'

long_description = (
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('collective', 'recipe', 'omelette', 'README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' + 
    read('CHANGES.txt')
    + '\n' +
    'Contributors\n' 
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Download\n'
    '********\n'
    )
entry_point = 'collective.recipe.omelette:Recipe'
uninstall_entry_point = 'collective.recipe.omelette:uninstall'

entry_points = {"zc.buildout": ["default = %s" % entry_point],
                "zc.buildout.uninstall": ["default = %s" % uninstall_entry_point]}

tests_require=['zope.testing', 'zc.recipe.egg']

setup(name='collective.recipe.omelette',
      version=version,
      description="Creates a unified directory structure of all namespace packages, symlinking to the actual contents, in order to ease navigation.",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='buildout eggs namespace',
      author='David Glick',
      author_email='davidglick@onenw.org',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'zc.buildout',
                        'zc.recipe.egg',
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'collective.recipe.omelette.tests.test_docs.test_suite',
      entry_points=entry_points,
      )
