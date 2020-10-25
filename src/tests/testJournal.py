#!/usr/bin/env python3

import sys

sys.path.insert(1, '..')

from journal import getLow, getHigh, append, flush, get, getRange
from record import Record

print(getLow())
print(getHigh())
rec = Record(transactionID= 1, messageType="Begin", key=1, operation= "inc")
print(rec.checkFormatCorrectness())
rec.key = None
rec.operation = None
rec.dependency = 22
rec.setTimestamp()
print(rec.checkFormatCorrectness())

id = append(rec)
print(id)
print(getHigh())
flush()
print(getHigh())
readRec = get(id)
assert rec == readRec

getRange(getHigh(), getLow())

