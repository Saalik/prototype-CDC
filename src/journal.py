import logging
import sys
import datetime
import time

from rainbowfs.logger import Logger
from utile import todo
from record import Record

journal = logging.getLogger()
journal.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(message)s')
ch.setFormatter(formatter)

log = Logger('journal')

current_time = lambda: int(round(time.time() * 1000))

fmt = '%d %s %s %s %s'

lowWatermark = log.id_low
highWatermark = log.id_high
assert lowWatermark <= highWatermark

def getLow():
    return lowWatermark

def getHigh():
    return highWatermark

def Append(record, sync=False):
    record.setTimestamp()
    log.append(record.toJournalEntry)
    if sync == True:
        log.flush()


    # if record.messageType == "Begin":
    #     entry = fmt % (current_time(), record.transactionID,
    #     record.messageType, record.dependency, None)
    #     log.append(entry)

    # elif record.messageType == "Update": 
    #     entry = fmt % (current_time(), record.transactionID,
    #     record.messageType, )
    #     log.asyncLog( transactionID, "Update", clock(), key, operation, None )
    

    # elif record.messageType == "Read":
    #     key = msgRecv[2]
    #     dependency = msgRecv[4]

    #     value = cache.get(key, dependency)
    #     assert value != None
    #     message = (self.shardID, transactionID, "Read", key, value)
    #     coordinator.send(message)

    # elif record.messageType == "Prepare":
    #     # Parsing the rest of the message 
    #     listOfParticipants = msgRecv[2]
    #     dependency = msgRecv[3]

    #     lsn = log.syncLog( transactionID , "Prepare", clock(),
    #     listOfParticipants, dependency )
    #     if lsn:
    #         updateHigh(lsn)
    #         acceptMessage = ( self.shardID, transactionID, "Accept", clock() )
    #         coordinator.send(acceptMessage)
    #     else:
    #         abortMessage = (self.shardID, transactionID, "Abort", clock() )
    #         coordinator.send(abortMessage)
        
    # elif record.messageType == "Commit":
    #     commitTime = msgRecv[2]
    #     dependency = msgRecv[3]
    #     lsn = log.asyncLog( transactionID , "Commit", commitTime )


    # elif record.messageType == "Abort":
    #     log.asyncLog( transactionID , "Abort", clock())

    # else :
    #     assert False
    # return None

def get(id):
    assert id > lowWatermark
    assert id < highWatermark
    entry = log.get(id)
    record = Record()
    record.fromEntry(entry)
    return record

def getRange(firstID, lastID):
    assert firstID < lastID
    assert firstID > lowWatermark
    assert firstID < highWatermark
    assert lastID > lowWatermark
    assert lastID < highWatermark  

    listOfRecords = []
    for i in range (firstID,lastID+1):
        entry = log.get(i)
        record = Record()
        record.fromEntry(entry)
        listOfRecords.append(record)
    return listOfRecords
