#!/usr/bin/env python3

import logging
import sys
import datetime
import time

sys.path.insert(1, 'log-api')
from rainbowfs.logger import Logger

journal = logging.getLogger()
journal.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(message)s')
ch.setFormatter(formatter)

l = Logger('journal')

current_time = lambda: int(round(time.time() * 1000))

trId = 0

fmt = '%d %s %s %s %s'

lowWatermark = l.id_low
highWatermark = l.id_high
assert low <= high
record = fmt % (current_time(), trId, "Begin", "dependency", " ")
n = l.append(record)

l.flush()
assert l.get(n) == record
assert l.get(lowWatermark-1) is None
assert l.get(highWatermark+1) is None
assert low <= high

for i in range(low, high):
    assert l.get(i) is not None

userInput = input("Do you wish to launch interactive mode? y/N ")
if userInput == "y":
    print("Type command in the following format:")
    print("Get the high watermark")
    print("high")
    print()
    print("Get the low watermark")
    print("low")
    print()
    print("Flush records")
    print("flush")
    print()
    print("Append record")
    print("append transactionID type arg1 arg2")
    print()
    print("Get record ")
    print("get recordID")
    print()

    while True:
        userInput = input()
        command = userInput.split()
        if not command:
            continue
        elif command[0] == "low":
            print(l.id_low)
        elif command[0] == "high":
            print(l.id_high)
        elif command[0] == "get":
            try: 
                int(command[1])
            except ValueError:
                print(command[1]+" is not a valid option")
            l.get(int(command[1]))
        elif command[0] == "append":
            if len(command) >= 4:
                record = fmt % (current_time(), command[1], command[2], command[3], 
                command[4] if len(command) == 5 else "None")
                l.append(record)
                if command[2] == "prepare":
                    l.flush()
        elif command[0] == "flush":
            l.flush()
            print("Records flushed")
        elif command[0] == "truncate":
            l.truncate(low)
        else:
            print("Wrong format")
