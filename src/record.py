from dataclasses import dataclass
from typing import Any
import pprint
import time
import sys


@dataclass
class Record:
    timestamp: Any = None
    messageType: Any = None
    transactionID: int = None
    key: str = None
    operation: str = None
    dependency: str = None
    listOfParticipants: Any = None
    commitTime: Any = None

    def setTimestamp(self):
        self.timestamp = int(round(time.time() * 1000))
    
    def toJournalEntry(self):
        entry = ""
        if self.timestamp == None:
            self.timestamp = int(round(time.time() * 1000))
        entry = entry + str(self.timestamp)
        
        if self.transactionID == None:
            sys.stderr.write("No transactionID in record, quitting \n")
            assert False
        entry = entry + " " + str(self.transactionID)
        
        if self.messageType == None:
            sys.stderr.write("No message type in record, quitting \n")
            assert False
        entry = entry + " " + self.messageType

        if self.key != None:
            entry = entry + " " + str(self.key)
        if self.operation != None:
            entry = entry + " " + self.operation
        if self.dependency != None:
            entry = entry + " " + self.dependency
        if self.listOfParticipants != None:
            entry = entry + " " + self.listOfParticipants
        if self.commitTime != None:
            entry = entry + " " + self.commitTime

        return entry

    def fromEntry (self, entry):
        information = entry.split()
        self.timestamp = information.pop(0)
        self.transactionID = information.pop(0)
        self.messageType = information.pop(0)

        if self.messageType == "Begin":
            self.dependency = information.pop(0)
        
        elif self.messageType == "Update":
            self.key = information.pop(0)
            self.operation = information.pop(0)
        
        elif self.messageType == "Prepare":
            self.dependency = information.pop(0)
            self.listOfParticipants = information.pop(0)

        elif self.messageType == "Commit":
            self.commitTime = information.pop(0)

        elif self.messageType == "Abort":
            None
        else:
            assert False

    def checkFormatCorrectness(self):
        if self.timestamp == None:
            return False
        if self.transactionID == None:
            return False
        if self.messageType == None:
            return False
        
        if self.messageType == "Begin":
            if self.dependency == None:
                return False
            else:
                return True
        
        elif self.messageType == "Update":
            if self.key == None or self.operation == None:
                return False
            else:
                return True
        
        elif self.messageType == "Prepare":
            if self.dependency == None or self.listOfParticipants == None:
                return False
            else:
                return True

        elif self.messageType == "Commit":
            if self.commitTime == None:
                return False
            else:
                return True
        
        elif self.messageType == "Abort":
            return True
        
        else:
            return False


