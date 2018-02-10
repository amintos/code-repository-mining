# This file belongs to the client application of github.com/flxw/code-repository-mining
# It encapsulates the platform differences when querying the installed software
import platform

distro = platform.linux_distribution()

def get_package_list():
  package_list = []

  if distro[0] == "arch":
    import pacman
    package_list = [ {
      "name":   p['id'],
      "version":p['version']
    } for p in pacman.get_installed() ]

  elif distro[0] == 'debian':
    import apt
    cache = apt.Cache()

    for pkg in apt.Cache():
      if cache[pkg.name].is_installed:
        package_list.append({
          "name":    pkg.name,
          "version": pkg.installed.version
        })
  else:
    print("Unsupported distribution right here!", file=sys.stderr)
    exit(1)

  return package_list
