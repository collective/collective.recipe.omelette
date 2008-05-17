# -*- coding: utf-8 -*-
"""
Doctest runner for 'collective.recipe.omelette'.
"""
__docformat__ = 'restructuredtext'

import os
import re
import unittest
import shutil
import zc.buildout.tests
import zc.buildout.testing

from zope.testing import doctest, renormalizing

optionflags =  (doctest.ELLIPSIS |
                doctest.NORMALIZE_WHITESPACE |
                doctest.REPORT_ONLY_FIRST_FAILURE)

test_dir = os.path.abspath(os.path.dirname(__file__))
test_path = 'collective/recipe/omelette/tests/'

def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)

    # Install the recipe (and dependencies) in develop mode
    zc.buildout.testing.install_develop('zc.recipe.egg', test)
    zc.buildout.testing.install_develop('collective.recipe.omelette', test)

def tearDown(test):
    zc.buildout.testing.buildoutTearDown(test)
    
    # get rid of the extra product directory that may have been created
    product_dir = test_dir + '/Products/Product3'
    if os.path.exists(product_dir):
        shutil.rmtree(product_dir)

def test_suite():
    suite = unittest.TestSuite((
            doctest.DocFileSuite(
                'omelette.txt',
                globs=globals(),
                setUp=setUp,
                tearDown=tearDown,
                optionflags=optionflags,
                checker=renormalizing.RENormalizing([
                        # If want to clean up the doctest output you
                        # can register additional regexp normalizers
                        # here. The format is a two-tuple with the RE
                        # as the first item and the replacement as the
                        # second item, e.g.
                        # (re.compile('my-[rR]eg[eE]ps'), 'my-regexps')
                        zc.buildout.testing.normalize_path,
                        
                        # don't count subversion dirs in ls() output
                        (re.compile(r'^\s*?d\s+.svn\s*?^', re.MULTILINE | re.DOTALL), ''),
                        ]),
                ),
            ))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
