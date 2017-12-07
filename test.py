#!/usr/bin/env python3

import platform

# check for linux distribution
distro = platform.linux_distribution()[0]

# depending on distro load appropriate package for interfacing
# with package management mechanism
if distro == "arch":
    import pacman
    
    package_list = pacman.get_installed()
    # for each package in package_list:
    # gather real package name
    print(package_list)
# do entity matching here
