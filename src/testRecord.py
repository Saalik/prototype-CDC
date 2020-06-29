#!/usr/bin/env python3

from record import Record


rec = Record(transactionID= 1, messageType="Counter", key=1, operation= "inc")
print(rec.transactionID)
print(rec.listOfParticipants)
rec.setTimestamp()
print(rec)
print(rec.toJournalEntry())

stringTest = rec.toJournalEntry()
print(stringTest)

newRec = Record()
print(newRec)
newRec.fromEntry(stringTest)
print(newRec)