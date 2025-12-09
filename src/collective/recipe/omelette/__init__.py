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

from os import symlink
from os.path import islink
from shutil import rmtree

import logging
import os
import sys
import zc.recipe.egg


WIN32 = sys.platform[:3].lower() == "win"


def makedirs(target):
    """Similar to os.makedirs, but stops when it encounters a link.

    Returns a boolean indicating success or failure.
    """
    drive, path = os.path.splitdrive(target)
    parts = path.split(os.path.sep)
    current = drive + os.path.sep
    for part in parts:
        current = os.path.join(current, part)
        if islink(current):
            return False
        if not os.path.exists(current):
            os.mkdir(current)
    return True


class Recipe:
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.logger = logging.getLogger(self.name)
        self.egg = zc.recipe.egg.Egg(buildout, options["recipe"], options)

        if "location" not in options:
            options["location"] = os.path.join(
                buildout["buildout"]["parts-directory"],
                self.name,
            )

        ignore_develop = options.get("ignore-develop", "").lower()
        develop_eggs = []
        if ignore_develop in ("yes", "true", "on", "1", "sure"):
            develop_eggs = os.listdir(buildout["buildout"]["develop-eggs-directory"])
            develop_eggs = [dev_egg[:-9] for dev_egg in develop_eggs]
        ignores = options.get("ignores", "").split()
        self.ignored_eggs = develop_eggs + ignores
        # In the tests we strangely have multiple versions of our own egg in the
        # working set.
        # 1. We have a dist with project name collective.recipe.omelette
        #    and location collective.recipe.omelette/src
        #   (so the src dir in the git repo).
        # 2. We have a dist with project name collective-recipe-omelette
        #    and location
        #    collective.recipe.omelette/.tox/test/lib/python3.13/site-packages
        # The first location has a collective directory in it, the second one not.
        # This causes a warning, which makes the tests fail:
        #   omelette: Warning: (While processing egg collective-recipe-omelette)
        #   Package 'collective' not found.  Skipping.
        # To avoid this, we ignore collective-recipe-omelette here.
        self.ignored_eggs += ["collective-recipe-omelette"]
        self.packages = [
            line.split()
            for line in options.get("packages", "").splitlines()
            if line.strip()
        ]

    def _install(self, location):
        requirements, ws = self.egg.working_set()
        for dist in ws.by_key.values():
            project_name = dist.project_name
            if project_name in self.ignored_eggs:
                continue
            namespaces = {}
            # Only pkg_resources-style namespace packages have a
            # namespace_packages.txt file.  I suppose pkgutil-style too.
            for line in dist._get_metadata("namespace_packages.txt"):
                ns = namespaces
                for part in line.split("."):
                    ns = ns.setdefault(part, {})
            if "." in project_name and not namespaces:
                # This is for implicit/native namespaces.
                ns = namespaces
                for part in project_name.split(".")[:-1]:
                    ns = ns.setdefault(part, {})

            top_level = sorted(list(dist._get_metadata("top_level.txt")))
            # native_libs = list(dist._get_metadata('native_libs.txt'))

            def create_namespaces(namespaces, ns_base=()):
                for k, v in namespaces.items():
                    ns_parts = ns_base + (k,)
                    link_dir = os.path.join(location, *ns_parts)
                    if not os.path.exists(link_dir):
                        if not makedirs(link_dir):
                            self.logger.warning(
                                "Warning: (While processing egg %s) Could not create namespace directory (%s).  Skipping.",
                                project_name,
                                link_dir,
                            )
                            continue
                    if islink(link_dir):
                        # For example, if you have packages one.two and one.three,
                        # here you may already have a link to
                        # .../lib/python3.12/site-packages/one/
                        return
                    if len(v) > 0:
                        create_namespaces(v, ns_parts)
                    egg_ns_dir = os.path.join(dist.location, *ns_parts)
                    if not os.path.isdir(egg_ns_dir):
                        self.logger.info(
                            "(While processing egg %s) Package '%s' is zipped.  Skipping.",
                            project_name,
                            os.path.sep.join(ns_parts),
                        )
                        continue
                    dirs = os.listdir(egg_ns_dir)
                    for name in dirs:
                        if name.startswith("."):
                            continue
                        name_parts = ns_parts + (name,)
                        src = os.path.join(dist.location, *name_parts)
                        dst = os.path.join(location, *name_parts)
                        if os.path.exists(dst):
                            continue
                        symlink(src, dst)

            create_namespaces(namespaces)
            for package_name in top_level:
                if package_name in namespaces:
                    # These are processed in create_namespaces
                    continue
                if not os.path.isdir(dist.location):
                    self.logger.info(
                        "(While processing egg %s) Package '%s' is zipped.  Skipping.",
                        project_name,
                        package_name,
                    )
                    continue

                package_location = os.path.join(dist.location, package_name)
                link_location = os.path.join(location, package_name)
                # check for single python module
                if not os.path.exists(package_location):
                    package_location = os.path.join(dist.location, package_name + ".py")
                    link_location = os.path.join(location, package_name + ".py")
                # check for native libs
                # XXX - this should use native_libs from above
                if not os.path.exists(package_location):
                    package_location = os.path.join(dist.location, package_name + ".so")
                    link_location = os.path.join(location, package_name + ".so")
                if not os.path.exists(package_location):
                    package_location = os.path.join(
                        dist.location, package_name + ".dll"
                    )
                    link_location = os.path.join(location, package_name + ".dll")
                if not os.path.exists(package_location):
                    self.logger.warning(
                        "Warning: (While processing egg %s) Package '%s' not found.  Skipping.",
                        project_name,
                        package_name,
                    )
                    continue
                if not os.path.exists(link_location):
                    if WIN32 and not os.path.isdir(package_location):
                        self.logger.warning(
                            "Warning: (While processing egg %s) Can't link files on Windows (%s -> %s).  Skipping.",
                            project_name,
                            package_location,
                            link_location,
                        )
                        continue
                    try:
                        symlink(package_location, link_location)
                    except OSError as e:
                        self.logger.warning(
                            "While processing egg (%s) symlink fails (%s, %s). Skipping.\nOriginal Exception:\n%s",
                            project_name,
                            package_location,
                            link_location,
                            str(e),
                        )
                    # except:
                    #    # TODO: clarify if recipe should fail on error or resume by skipping.
                    #    # Possible solution, add a recipe option, stop_on_fail that will quit buildout on general exceptions
                    #    self.logger.warning("Unexpected error :\nWhile processing egg %s) symlink fails (%s, %s). Skipping.\nOriginal Exception:\n%s", project_name, package_location, link_location, sys.exc_info()[0])
                else:
                    self.logger.info(
                        "(While processing egg %s) Link already exists (%s -> %s).  Skipping.",
                        project_name,
                        package_location,
                        link_location,
                    )
                    continue

        for package in self.packages:
            if len(package) == 1:
                link_name = "./"
                package_dir = package[0]
            elif len(package) == 2:
                link_name = package[1]
                package_dir = package[0]
            else:
                self.logger.warning(
                    "Warning: Invalid package: %s %s", self.name, package
                )
                continue

            link_dir = os.path.join(location, link_name)
            self._add_bacon(package_dir, link_dir)

    def install(self):
        """Crack the eggs open and mix them together"""

        location = self.options["location"]
        if os.path.exists(location):
            rmtree(location)
        os.mkdir(location)

        try:
            self._install(location)
        except Exception:
            if os.path.exists(location):
                rmtree(location)
            raise

        return location

    update = install

    def _add_bacon(self, package_dir, target_dir):
        """Link packages from package_dir into target_dir.  Recurse a level if target_dir/(package)
        already exists.
        """
        if not os.path.exists(package_dir):
            self.logger.warning(
                "Warning: Product directory %s not found.  Skipping.", package_dir
            )

        if islink(target_dir):
            self.logger.warning(
                "Warning: (While processing package directory %s) Link already exists at %s.  Skipping.",
                package_dir,
                target_dir,
            )
            return

        if not os.path.exists(target_dir) and not makedirs(target_dir):
            self.logger.warning(
                "Warning: (While processing package directory %s) Link already exists at %s.  Skipping.",
                package_dir,
                target_dir,
            )
            return

        for package_name in [
            p for p in os.listdir(package_dir) if not p.startswith(".")
        ]:
            package_location = os.path.join(package_dir, package_name)
            if not os.path.isdir(package_location):
                # skip ordinary files
                continue
            link_location = os.path.join(target_dir, package_name)
            if islink(link_location):
                self.logger.warning(
                    "Warning: (While processing package %s) Link already exists.  Skipping.",
                    package_location,
                )
            elif os.path.isdir(link_location):
                self._add_bacon(package_location, link_location)
            else:
                symlink(package_location, link_location)


def uninstall(name, options):
    location = options.get("location")
    if os.path.exists(location):
        rmtree(location)
