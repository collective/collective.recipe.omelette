Introduction
============

Namespace packages offer the huge benefit of being able to distribute parts of a large
system in small, self-contained pieces.  However, they can be somewhat clunky to navigate,
since you end up with a large list of eggs in your egg cache, and then a seemingly endless
series of directories you need to open to actually find the contents of your egg.

This recipe sets up a directory structure that mirrors the actual python namespaces, with
symlinks to the egg contents.  So, instead of this...::

    egg-cache/
        my.egg.one-1.0-py2.4.egg/
            my/
                egg/
                    one/
                        (contents of first egg)
        my.egg.two-1.0-py2.4.egg/
            my/
                egg/
                    two/
                        (contents of second egg)

...you get this::

    omelette/
        my/
            egg/
                one/
                    (contents of first egg)
                two/
                    (contents of second egg)


**Caveat 1**: Don't try to manually add any eggs to the omelette!

**Caveat 2**: This only works with filesystems that support symlinks (so no go on Windows).


Supported options
=================

The recipe supports the following options:

eggs
    List of eggs which should be included in the omelette.

location
    (optional) Override the directory in which the omelette is created (default is parts/[name of buildout part])

ignore-develop
    (optional) Ignore eggs that you are currently developing (listed in ${buildout:develop}). Default is False

ignores
    (optional) List of eggs to ignore when preparing your omelette.
    
products
    (optional) List of old Zope 2-style products directories whose contents should be included in the omelette,
    in a directory called Products.
    

Example usage
=============

Usage is pretty basic.  The following installs a buildout and omelette featuring the
setuptools egg (for the sake of example, since it has no dependencies)::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... eggs = setuptools
    ... parts = omelette
    ...
    ... [omelette]
    ... recipe = collective.recipe.omelette
    ... eggs = ${buildout:eggs}
    ... """)

Running the buildout gives us::

    >>> print system(buildout)
    Installing omelette.
    <BLANKLINE>

Now we have an easily navigable link::

    >>> import os
    >>> os.path.exists('parts/omelette/setuptools')
    True
    >>> ls('parts/omelette')
    d setuptools

And it points to the real location of the egg's contents::

    >>> os.readlink('parts/omelette/setuptools')
    '/sample-buildout/eggs/setuptools-....egg/setuptools'
    
You can also include old-style Products directories in the omelette (for Zope developers)::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts =
    ...     productdistros
    ...     omelette
    ... 
    ... [productdistros]
    ... recipe = plone.recipe.distros
    ... urls = http://plone.org/products/pressroom/releases/3.1/pressroom-3-1.tgz
    ...
    ... [omelette]
    ... recipe = collective.recipe.omelette
    ... products =
    ...     ${productdistros:location}
    ...     ${buildout:directory}/duplicate-product-test
    ... """)
    >>> mkdir('duplicate-product-test')
    >>> mkdir('duplicate-product-test/PressRoom')
    >>> print system(buildout + ' -q')

Any subdirectories of the products directories will be added to the omelette::

    >>> ls('parts/omelette/Products')
    d PressRoom
    
If a subdirectory of the same name appears in two different product directories,
the first one encountered will take precedence::

    >>> os.readlink('parts/omelette/Products/PressRoom')
    '/sample-buildout/parts/productdistros/PressRoom'

If we call the part something else, the omelette should be created there instead
(and the old one removed)::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... eggs = setuptools
    ... parts = frittata
    ...
    ... [frittata]
    ... recipe = collective.recipe.omelette
    ... eggs = ${buildout:eggs}
    ... """)
    >>> print system(buildout + ' -q')
    >>> os.path.exists('parts/omelette')
    False
    >>> os.path.exists('parts/frittata')
    True

You can also override the location of the omelette if you want to put it
somewhere else entirely::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... eggs = setuptools
    ... parts = omelette
    ...
    ... [omelette]
    ... recipe = collective.recipe.omelette
    ... eggs = ${buildout:eggs}
    ... location = ${buildout:directory}/omelette
    ... """)
    >>> print system(buildout + ' -q')
    >>> os.path.exists('omelette')
    True

You can ignore a particular package::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... eggs = setuptools
    ... parts = omelette
    ...
    ... [omelette]
    ... recipe = collective.recipe.omelette
    ... eggs = ${buildout:eggs}
    ... ignores = setuptools
    ... """)
    >>> print system(buildout + ' -q')
    >>> os.path.exists('parts/omelette/setuptools')
    False
    
Or ignore all development eggs::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... eggs = collective.recipe.omelette
    ... parts = omelette
    ...
    ... [omelette]
    ... recipe = collective.recipe.omelette
    ... eggs = ${buildout:eggs}
    ... ignore-develop = true
    ... """)
    >>> print system(buildout + ' -q')
    >>> ls('parts/omelette')
    d setuptools
    d zc

Running the tests
=================

The subversion checkout of collective.recipe.omelette includes a buildout
which installs a script for running the tests.

Just run::
    python2.4 bootstrap.py
    bin/buildout
    bin/test

Known issue: The tests run buildout in a separate process, so it's currently
impossible to put a pdb breakpoint in the recipe and debug during the test.
If you need to do this, set up another buildout which installs an omelette
part and includes collective.recipe.omelette as a development egg.


Reporting bugs or asking questions
==================================

There is a shared bugtracker and help desk on Launchpad:
https://bugs.launchpad.net/collective.buildout/
