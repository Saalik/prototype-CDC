#!/usr/bin/env python3

import logging
import sys
import datetime
import time
import os

sys.path.insert(1, '..')
from record import Record
from logger.logger import Logger

userInput = input("Do you wish to reset data ? y/N\n")
if userInput == "y":
    os.system("rm -r ../journal/")   

journal = logging.getLogger()
journal.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(message)s')
ch.setFormatter(formatter)

l = Logger('../journal')

current_time = lambda: int(round(time.time() * 1000))

trId = 0

fmt = '%d %s %s %s %s'

print("Starting log")

lowWatermark = l.id_low
highWatermark = l.id_high
assert lowWatermark <= highWatermark
record = fmt % (current_time(), trId, "Begin", "dependency", " ")
n = l.append(record)

l.flush()
assert l.get(n) == record
assert l.get(lowWatermark-1) is None
assert l.get(highWatermark+1) is None
assert lowWatermark <= highWatermark

for i in range(lowWatermark, highWatermark):
    assert l.get(i) is not None

userInput = input("Do you wish to launch interactive mode? y/N ")
if userInput == "y":
    print("\nHow to use the journal :\n")
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
    print("Exit")
    print("exit")

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
            record = l.get(int(command[1]))
            print(record)
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
            l.truncate(lowWatermark)
        elif command[0] == "exit":
            break
        else:
            print("Wrong format")

print("Test ended")