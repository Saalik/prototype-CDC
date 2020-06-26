import logging
import sys
import datetime
import time

from rainbowfs.logger import Logger
from utile import todo

journal = logging.getLogger()
journal.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(message)s')
ch.setFormatter(formatter)

l = Logger('journal')

current_time = lambda: int(round(time.time() * 1000))

trId = 0

fmt = '%d:%s:%s:%s'

low = l.id_low
high = l.id_high
assert low <= high

def low():
    return low

def high():
    return high

def syncAppend(record):
    todo("journal.py-syncAppend not impemented")
    return None

def asyncAppend(record):
    todo("journal.py-asyncAppend not impemented")
    return None

def get(id):
    rawRecord = l.get(id)
    todo("journal.py-get(id) not impemented")
    return rawRecord

def getRange(beginID, lastID):
    todo("journal.py-getRange not impemented")
    return None
