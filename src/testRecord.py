#!/usr/bin/env python3

from record import Record
import time

current_time = lambda: int(round(time.time() * 1000))

rec = Record(transactionID= 1, messageType="Begin", key=1, operation= "inc")
print("TransactionID "+str(rec.transactionID))
print("List Of Participants "+ str(rec.listOfParticipants))
print(rec.checkFormatCorrectness())
rec.setTimestamp()
print("Timestamp " + str(rec.timestamp))
print()
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
