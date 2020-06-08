#!/usr/bin/env python3

import os
# from manager import Manager


# print("Starting DB")
# print("How many shards do you want to create?")
# print("Please enter a number")
# while (True):
#     inputNbShard = input()
#     if(inputNbShard.isnumeric()):
#         break
#     print(inputNbShard+" is not a valid entry")
# assert inputNbShard > 0
# dbManager = Manager(inputNbShard)

print("Starting log")

userInput = input("Do you wish to reset data ? ")
if userInput == "y":
    os.system("rm -r journal/")    
os.system("docker build log-api -t rainbowfs-log-api")
os.system("docker run --rm rainbowfs-log-api")