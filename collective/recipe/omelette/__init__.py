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
import sys
import shutil
import zc.recipe.egg

WIN32 = False
if sys.platform[:3].lower() == "win":
    WIN32 = True

if WIN32:
    
    # We assume this is in the system PATH. The commands will fail if it's not.
    JUNCTION = "junction.exe" 
    
    def symlink(src, dest):
        cmd = "%s %s %s" % (JUNCTION, os.path.abspath(dest), os.path.abspath(src),)
        os.system(cmd)

    def unlink(dest):
        cmd = "%s -d %s" % (JUNCTION, os.path.abspath(dest),)
        os.system(cmd)

    def islink(dest):
        cmd = "%s %s" % (JUNCTION, os.path.abspath(dest),)
        stdout = os.popen(cmd)
        output = stdout.read()
        stdout.close()
        return "Substitute Name:" in output
        
        
    def rmtree(location):
        # Explicitly unlink all junction'd links
        for root, dirs, files in os.walk(location, topdown=False):
            for dir in dirs:
                path = os.path.join(root, dir)
                if islink(path):
                    unlink(root)
        # Then get rid of everything else
        shutil.rmtree(location)
        
else:
    symlink = os.path.symlink
    islink = os.path.islink
    rmtree = shutil.rmtree

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
            develop_eggs = [dev_egg[:-9] for dev_egg in develop_eggs]
        ignores = options.get('ignores', '').split()
        self.ignored_eggs = develop_eggs + ignores
        self.products = [l.split()
                         for l in options['products'].splitlines()
                         if l.strip()]

    def install(self):
        """Crack the eggs open and mix them together"""
        
        location = self.options['location']
        if os.path.exists(location):
            rmtree(location)
        
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
                    if not os.path.exists(egg_location):
                        print "[collective.recipe.omelette] Warning: (While processing egg %s) Egg contents not found at %s.  Skipping." % (project_name, egg_location)
                        continue
                    if not os.path.exists(link_location):
                        symlink(egg_location, link_location)
                    else:
                        print "[collective.recipe.omelette] Warning: (While processing egg %s) Link already exists.  Skipping." % project_name
                    
            for product in self.products:
                if len(product) == 1:
                    link_name = 'Products/'
                    product_dir = product[0]
                elif len(product) == 2:
                    link_name = product[1]
                    product_dir = product[0]
                else:
                    print "[collective.recipe.omelette] Warning: Invalid value in ${%s:products}: %s" % (self.name, product)
                
                link_dir = os.path.join(location, link_name)
                self._add_bacon(product_dir, link_dir)
                            
        except:
            if os.path.exists(location):
                rmtree(location)
            raise
        
        return location
        
    def _add_bacon(self, product_dir, target_dir):
        """ Link products from product_dir into target_dir.  Recurse a level if target_dir/(product)
            already exists.
        """
        if os.path.exists(product_dir):
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            for product_name in [p for p in os.listdir(product_dir) if not p.startswith('.')]:
                product_location = os.path.join(product_dir, product_name)
                if not os.path.isdir(product_location):
                    # skip ordinary files
                    continue
                link_location = os.path.join(target_dir, product_name)
                if islink(link_location):
                    print "[collective.recipe.omelette] Warning: (While processing product %s) Link already exists.  Skipping." % product_location
                elif os.path.isdir(link_location):
                    self._add_bacon(product_location, link_location)
                else:
                    symlink(product_location, link_location)
        else:
            print "[collective.recipe.omelette] Warning: Product directory %s not found." % product_dir
        
    def update(self):
        pass
