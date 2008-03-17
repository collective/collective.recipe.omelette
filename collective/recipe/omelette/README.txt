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
    Override the directory in which the omelette is created (default is parts/[name of buildout part])

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
    Upgraded:
    ...
    Installing omelette.
    <BLANKLINE>

Now we have an easily navigable link::

    >>> import os
    >>> os.path.exists('parts/omelette/setuptools')
    True

And it points to the real location of the egg's contents::

    >>> os.readlink('parts/omelette/setuptools')
    '/sample-buildout/eggs/setuptools-....egg/setuptools'

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
    >>> print system(buildout)
    Uninstalling...
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
    >>> print system(buildout)
    Uninstalling...
    >>> os.path.exists('omelette')
    True

Reporting bugs or asking questions
==================================

There is a shared bugtracker and help desk on Launchpad:
https://bugs.launchpad.net/collective.buildout/
