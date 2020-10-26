import socket
import twopc
import select
from recovery import *
import time
import coordinator
from logging import log
from manager import Manager
from utile import todo
from journal import get
from journal import getLow
from journal import getHigh
from journal import append
from record import Record


class Shard:
    def __init__(self, id, dcManager):
        self.shardID = None
        self.journal = None
        self.recoveryInformation = None
        self.highWatermark = None
        self.lowWatermark = None
        self._lock = threading.Lock()
        self.shardID = id
        # print("Shard "+str(id)+" starting intialization")
        # self.dcManager = dcManager
        # dcManager.testConnection("This is "+str(id))
        journal = "journal" + id
        self.journal = journal.get()
        if not (journal == journal.empty()):
            self.recoveryInformation = recovery.recovery(journal)
            self.highWatermark = self.recoveryInformation.highWatermark
            self.lowWatermark = self.recoveryInformation.lowWatermark
        else:
            self.highWatermark = 0
            self.lowWatermark = 0

        assert self.lowWatermark <= self.highWatermark

        self.receive()

    # def checkInvariants():
    #     assert lowWatermark <= highWatermark

    def receive(self):
        msgRecv = None
        mysocket = None

        while True:
            msgRecv = None
            ready = select.select([mysocket], [], [], TIMEOUT)
            if ready[0]:
                msgRecv = socket.recv()
            else:
                interdc.sendHeartbeat(self.ShardID)
                continue
            trID = msgRecv[0]
            messageType = msgRecv[1]

            if messageType == "Begin":
                dependency = msgRecv[4]
                record = Record(messageType="Begin", transactionID=trID)
                append(record)

            elif messageType == "Update":
                key = msgRecv[2]
                operation = msgRecv[3]
                dependency = msgRecv[4]
                record = Record(
                    transactionID=trID,
                    messageType="Update",
                    key=key,
                    operation=operation,
                    dependency=dependency,
                )
                append(record)

            elif messageType == "Read":
                key = msgRecv[2]
                dependency = msgRecv[4]

                value = cache.get(key, dependency)
                assert value != None
                message = (self.shardID, trID, "Read", key, value)
                coordinator.send(message)

            elif messageType == "Prepare":
                # Parsing the rest of the message
                listOfParticipants = msgRecv[2]
                dependency = msgRecv[3]

                lsn = log.syncLog(trID, "Prepare", dependency, listOfParticipants)
                if lsn:
                    updateHigh()
                    acceptMessage = (self.shardID, trID, "Accept")
                    coordinator.send(acceptMessage)
                else:
                    abortMessage = (self.shardID, trID, "Abort")
                    coordinator.send(abortMessage)

            elif messageType == "Commit":
                commitTime = msgRecv[2]
                dependency = msgRecv[3]
                lsn = log.asyncLog(trID, "Commit", commitTime)

            elif messageType == "Abort":
                log.asyncLog(trID, "Abort")
            elif messageType == "NewParticipant":
                todo("New participant message handling missing from shard")

            else:
                assert False

    def updateHigh():
        newValue = getHigh()
        assert lowWatermark <= highWatermark
        with self._lock:
            if self.highWatermark < newValue:
                self.highWatermark = newValue
        assert lowWatermark <= highWatermark

    def updateLow():
        newValue = getLow()
        assert lowWatermark <= highWatermark
        with self._lock:
            if self.lowWatermark < newValue:
                self.lowWatermark = newValue
        assert lowWatermark <= highWatermark


# Message format expected for an update
# # { TransactionID, Type, Key, operation, Dependency }
# Record Format
# # { Log Sequence Number,Transaction ID, Clock, Key, Operation, Dependency}

# Message format expected for a read
# # {TransactionID, Type, Key, None, Dependency }
# No RYOW in this algorithm for now

# Message format expected for the Prepare message
# # { Transaction ID, "Prepare", List of Participants, Dependency }
# Accept message sent in the following format
# # { Participant ID, Transaction ID, Message, Value
