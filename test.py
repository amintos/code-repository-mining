#!/usr/bin/env python3

import platform

# check for linux distribution
distro = platform.linux_distribution()
package_list = []

# depending on distro load appropriate package for interfacing
# with package management mechanism
if distro[0] == "arch":
  import pacman
  package_list = [ {"id":p['id'], "version":p['version']} for p in pacman.get_installed() ]

elif distro[0] == 'debian':
  import apt
  cache = apt.Cache()

  for pkg in apt.Cache():
    if cache[pkg.name].is_installed:
      package_list.append({
        "id": pkg.id,
        "version": pkg.installed.version
      })

# do entity matching here
print(package_list)