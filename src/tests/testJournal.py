#!/usr/bin/env python3

import sys

sys.path.insert(1, '..')

from journal import getLow, getHigh, append, flush, get, getRange
from record import Record


print("This is a test of src/journal.py")
print("Checks the values of LowWatermark and HighWatermark")
print("Creates a record and checks the format correctness using record.py")
print("Append the record to the journal")
print("The record is then flushed")


print("LowWatermark is "+ str(getLow()) )
print("HighWatermark is "+ str(getHigh()) )
print("Creating the record")
rec = Record(transactionID= 1, messageType="Begin", key=1, operation= "inc")
print(rec)
print("Format correctness: "+str(rec.checkFormatCorrectness())+"\n")
# rec.key = None
# rec.operation = None
# rec.dependency = 22
# rec.setTimestamp()
# print(rec.checkFormatCorrectness())

id = append(rec)
print("Appending the record : "+str(id))
print("Checking High before flush " + str(getHigh()))
flush()
print("Checking High after flush " +str(getHigh()))
print("Retrieving record from the journal")
readRec = get(id)
#readsec = get(id+1)
print("Reading the high" + str(getHigh()))
print("Checking if retrieved record matches written record")
print("WrittenRec == ReadRecord : " + str(rec == readRec))


