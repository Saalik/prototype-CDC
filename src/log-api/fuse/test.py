#!/usr/bin/env python

import os
from sys import platform

# Mounts 

# Replace this with the folder you want to mount
LOCALDIR = "/Users/saalik/OneDrive/PhD/code/prototype-CDC/src/log-api/fuse/journal"

if platform == "linux" or platform == "linux2":
    os.system("python3 myfuse.py LOCALDIR /mnt/journal")
elif platform == "darwin":
    os.system("python3 myfuse.py LOCALDIR /Volumes/journal")
else:
    print("Windows is not supported")


os.system("python3 myfuse.py LOCALDIR /Volumes/journal")

python3 myfuse.py /Users/saalik/OneDrive/PhD/code/prototype-CDC/src/log-api/fuse/journal /mnt/journal


