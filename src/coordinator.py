import select
import socket
import twopc

# This transaction coordinatoor is created when a new transaction
# is started

# It waits for new operations and forwards them to
# the appropriate shard

# Once it receives the commit message
# calls the initCommit function from 2PC
# Once the commit is done the coordinator is terminated
TIMEOUT = 600


class coordinator:

    # Constructor
    # Take the transaction id and the dependency as parameters
    def __init__(self, transactionID, dependency, client):
        self.transactionID = transactionID
        self.dependency = dependency
        self.listOfParticipants = set()
        self.client = client
        receive()

    def receive(self):
        msgRecv = None
        while True:

            ready = select.select([mysocket], [], [], TIMEOUT)
            if ready[0]:
                msgRecv = socket.recv()
            else:
                if len(self.listOfParticipants) != 0:
                    assert twopc.initAbort(transactionID, listOfParticipants)
                return

            receivedTransactionID = msgRecv[1]
            typeOfMessage = msgRecv[2]
            assert receivedTransactionID == self.transactionID

            if typeOfMessage == "update":
                key = msgRecv[3]
                operation = msgRecv[4]
                participant = getShardFromKey(key)
                if not (participant in self.listOfParticipants):
                    self.listOfParticipants.add(participant)
                    beginMsg = (
                        self.transactionID,
                        "begin",
                        None,
                        None,
                        self.dependency,
                    )
                    participant.send(beginMsg)
                updateMsg = (
                    self.transactionID,
                    typeOfMessage,
                    key,
                    operation,
                    self.dependency,
                )
                participant.send(updateMsg)

            elif typeOfMessage == "read":
                msgRecv = None
                key = msgRecv[2]
                participant = getShardFromKey(key)
                readQuery = (
                    self.transactionID,
                    typeOfMessage,
                    key,
                    None,
                    self.dependency,
                )
                participant.send(readQuery)

                while msgRecv != None:
                    ready = select.select([mysocket], [], [], TIMEOUT)
                    if ready[0]:
                        msgRecv = socket.recv()
                    else:
                        participant.send(readQuery)

                # Message format expected
                # (Shard ID, Transaction ID, Message Type, key, value)
                key = msgRecv[3]
                value = msgRecv[4]
                readValue = (self.transactionID, "read", key, value)
                self.client(readValue)

            elif typeOfMessage == "commit":
                assert twopc.initCommit(transactionID, listOfParticipants, dependency)
                ackCommitMsg = (self.transactionID, "ack")
                self.client()
                return

            else:
                assert False

    # Each operation is sent to relevent
    # shard, that shard is added to listof participans
    # of this transaction.
