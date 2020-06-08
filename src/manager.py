from shard import Shard
from utile import todo
# TODO
# Created when the database is started or reboot
# Initiate each shard 
# Then wait for lists from shard recoveries
# check the lists 
# If needed run initAbort
# If needed run initcommit
# If needed send commit messages to shards


# Wait for clients
# When a new clients connects
# create a new coordinator for the clients transaction
# When operation arrive transfer them to the coordinator

class Manager:
    def __init__(self, numberOfShard):
        # Init shards
        self.listOfShard = {}
        self.listOfRecoveryInformation = {}
        for i in range(int(numberOfShard)):
            createdShard = Shard(i)
            self.listOfRecoveryInformation[i] = createdShard.recoveryInformation
            self.listOfShard[i]= createdShard

        # Handle the answers from the recovery
        self.setOfTransactionsToAbort = set()
        self.setofTransactionsWithoutCommit = set()
        for recoveryInformation in self.listOfRecoveryInformation:
            transactionsToAbort = recoveryInformation.transactionsToAbort
            transactionsWithoutCommit = recoveryInformation.transactionsWithoutCommit
            self.setOfTransactionsToAbort = self.setOfTransactionsToAbort.union(transactionsToAbort)
            self.setofTransactionsWithoutCommit = self.setofTransactionsWithoutCommit.union(transactionsWithoutCommit)

        


        # Start receiving msg from clients
        self.receive

    def receive(self):
        todo()