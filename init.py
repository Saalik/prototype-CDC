#!/usr/bin/env python3
from manager import Manager


print("Starting DB")
print("How many shards do you want to create?")
print("Please enter a number")
while (True):
    inputNbShard = input()
    if(inputNbShard.isnumeric()):
        break
    print(inputNbShard+" is not a valid entry")

dbManager = Manager(inputNbShard)
