import socket
import twopc
import select
import recovery
from time import clock
import coordinator
from logging import log
from manager import Manager
from utile import todo

class Shard:

    def __init__(self, id, dcManager):
        self.shardID = None
        self.journal = None
        self.recoveryInformation = None
        self.highWatermark = None
        self.lowWatermark = None
        self._lock = threading.Lock()
        self.shardID = id
        #print("Shard "+str(id)+" starting intialization")
        #self.dcManager = dcManager
        #dcManager.testConnection("This is "+str(id))
        journalName = "journal"+id
        self.journal = journal.get()
        if not (journal == journal.empty()):
            self.recoveryInformation = recovery.recovery(journal)
            self.highWatermark = self.recoveryInformation.highWatermark
            self.lowWatermark = self.recoveryInformation.lowWatermark
        else :
            self.highWatermark = 0
            self.lowWatermark = 0

        assert self.lowWatermark <= self.highWatermark

        self.receive()

    def checkInvariants():
        assert lowWatermark <= highWatermark

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
            transactionID = msgRecv[0]
            messageType = msgRecv[1]

            if messageType == "Begin":
                dependency = msgRecv[4]
                log.asyncLog( transactionID, "Begin", clock() )

            elif messageType == "Update":
                key = msgRecv[2]
                operation = msgRecv[3]
                dependency = msgRecv[4]    
                log.asyncLog( transactionID, "Update", clock(), key, operation, None )
            

            elif messageType == "Read":
                key = msgRecv[2]
                dependency = msgRecv[4]

                value = cache.get(key, dependency)
                assert value != None
                message = (self.shardID, transactionID, "Read", key, value)
                coordinator.send(message)
                fo

            elif messageType == "Prepare":
                # Parsing the rest of the message 
                listOfParticipants = msgRecv[2]
                dependency = msgRecv[3]

                lsn = log.syncLog( transactionID , "Prepare", clock(),
                listOfParticipants, dependency )
                if lsn:
                    updateHigh(lsn)
                    acceptMessage = ( self.shardID, transactionID, "Accept", clock() )
                    coordinator.send(acceptMessage)
                else:
                    abortMessage = (self.shardID, transactionID, "Abort", clock() )
                    coordinator.send(abortMessage)
                
            elif messageType == "Commit":
                commitTime = msgRecv[2]
                dependency = msgRecv[3]
                lsn = log.asyncLog( transactionID , "Commit", commitTime )


            elif messageType == "Abort":
                log.asyncLog( transactionID , "Abort", clock())

            else :
                assert False
 

    def updateHigh( newValue ):
        assert lowWatermark <= highWatermark
        with self._lock:
            if (self.highWatermark < lsn):
                self.highWatermark = lsn
        assert lowWatermark <= highWatermark

    def updateLow( newValue ):
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
# # { Participant ID, Transaction ID, Message, Value }