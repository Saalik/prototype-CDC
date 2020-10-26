#!/usr/bin/env python3

import os

print("Starting log")

userInput = input("Do you wish to reset data ? ")
if userInput == "y":
    os.system("rm -r journal/")    