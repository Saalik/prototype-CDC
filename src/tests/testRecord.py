#!/usr/bin/env python3

import time
import sys

sys.path.insert(1, '..')

from record import Record

current_time = lambda: int(round(time.time() * 1000))

rec = Record(transactionID= 1, messageType="Begin", key=1, operation= "inc")
print("Transaction created\n"+str(rec)+"\n")

print("Checking is the format of the record is correct \nShould be false because there is no timestamps")
print(rec.checkFormatCorrectness())

print("Adding messing a timestamp to the record")
rec.setTimestamp()
print("Timestamp is " + str(rec.timestamp))
print("Checking again now that timestamp is added")
print(rec.toJournalEntry())

stringTest = rec.toJournalEntry()
print(stringTest)

secondRec = Record()
print(secondRec)
secondRec.fromEntry(stringTest)
print(secondRec)
print()
print(secondRec.checkFormatCorrectness())

secondRec.setMessageType("nothing")
