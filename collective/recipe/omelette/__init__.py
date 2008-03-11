# -*- coding: utf-8 -*-

##############################################################################
#
# Copyright (c) 2008 David Glick.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

"""
This recipe creates an easily navigable directory structure linking to the
contents of a lists of eggs.  See README.txt for details.
"""

import os, shutil

from zc.buildout import UserError
import zc.recipe.egg

class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.egg = zc.recipe.egg.Egg(buildout, options['recipe'], options)
        self.buildout, self.name, self.options = buildout, name, options
        
        options['location'] = os.path.join(
            buildout['buildout']['parts-directory'],
            self.name,
            )

    def install(self):
        """Crack the eggs open and mix them together"""
        
        location = self.options['location']
        
        if os.path.exists(location):
            shutil.rmtree(location)
        
        try:
            requirements, ws = self.egg.working_set()
            for name, dist in ws.by_key.items():
            
                parts = name.split('.')
                namespaces = parts[:-1]
                package_name = parts[-1]
                egg_location = os.path.join(dist.location, *parts)
            
                link_dir = os.path.join(location, *namespaces)
                if not os.path.exists(link_dir):
                    os.makedirs(link_dir)
                link_location = os.path.join(link_dir, package_name)
                os.symlink(egg_location, link_location)
        except:
            shutil.rmtree(location)
            raise
        
        return location

    def update(self):
        pass
