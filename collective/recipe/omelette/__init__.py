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

import os
import shutil
import zc.recipe.egg

class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.egg = zc.recipe.egg.Egg(buildout, options['recipe'], options)
        self.buildout, self.name, self.options = buildout, name, options
        
        if not options.has_key('location'):
            options['location'] = os.path.join(
                buildout['buildout']['parts-directory'],
                self.name,
                )
        ignore_develop = options.get('ignore-develop', '').lower()
        develop_eggs = []
        if ignore_develop in ('yes', 'true', 'on', '1', 'sure'):
            develop_eggs = os.listdir(
                               buildout['buildout']['develop-eggs-directory'])
            develop_eggs = [dev_egg.rstrip('.egg-link')
                            for dev_egg in develop_eggs]
        ignores = options.get('ignores', '').split()
        self.ignored_eggs = develop_eggs + ignores

    def install(self):
        """Crack the eggs open and mix them together"""
        
        location = self.options['location']
        if os.path.exists(location):
            shutil.rmtree(location)
        
        try:
            requirements, ws = self.egg.working_set()
            for dist in ws.by_key.values():
                project_name =  dist.project_name
                if  project_name not in self.ignored_eggs:
                    parts = project_name.split('.')
                    namespaces = parts[:-1]
                    package_name = parts[-1]
                    egg_location = os.path.join(dist.location, *parts)
                    
                    link_dir = os.path.join(location, *namespaces)
                    if not os.path.exists(link_dir):
                        os.makedirs(link_dir)
                    link_location = os.path.join(link_dir, package_name)
                    os.symlink(egg_location, link_location)
        except:
            if os.path.exists(location):
                shutil.rmtree(location)
            raise
        
        return location

    def update(self):
        pass
