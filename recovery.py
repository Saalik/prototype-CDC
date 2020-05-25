# Recovery
# 
# Description: After a crash or a restarted. 
# The database needs to reconstruct a coherent view from 
# the journal.
#
# Problem: The journal contains information from transactions that are
# both terminated or were running.
# With only the log we need find the following information and finish task:
# - Last checkpoint time
# - Transactions that need their commit process to be completed
# - Transaction that couldn't be committed by the client and write abort message
# - The last LogSequenceNumber 
# - High and low watermark

# Context:
# This function is called after a restart of the database
# Regardless of it being due to a crash or not
# It is called if a journal already exist in a Shard
# If there is no journal a new journal is created and this function is never called

# Disclaimer: This first version will do one task at time 
# No effort in optimization is present in this work

def recovery(journal):

# First we initialize the variables we will return
    # Last recorded Checkpoint Time
    checkpointTime = 0

    # High and low watermarks
    highWatermark = -1
    lowWatermark = -1

    # TransactionIDs sets 
    committed = set()
    prepared = set()
    transactionIDs = set()

    # First we get the LogSequenceNumber of the last record in the journal
    for record in journal:
        highWatermark = record.LogSequenceNumber
        assert highWatermark == record.LogSequenceNumber
    assert highWatermark > -1

    # We read all the records to find a checkpoint record
    # Everytime we find a record of a checkpoint we record the time
    # It is possible for checkpointTime to be 0
    # If so it means that no checkpoint is recorded
    # Assumption: checkpoint are Ordered
    for record in journal:
        if record.getType() == "System" and record.getOperation() == "Checkpoint":
            assert record.getTime() > checkpointTime
            checkpointTime = record.getTime()
            assert record.getTime() == checkpointTime
            

    # Now that we have the checkpoint time we can find the low watermark
    # We assume that if a checkpoint has been made the transactions included in the
    # checkpoint are terminated
    if checkpointTime > 0:
        for record in journal:
            if record.getTimestamp() < checkpointTime:
                if record.getType() == "System" and record.getOperation() == "Commit":
                    committed.add(record.getTransactionID())
            else :
                assert record.getTimestamp() >= checkpointTime
                break

    # We now have all the transactionIDs of terminated transactions

    # We read the log again find the first record that has a
    # transactionID that is not present in committed is the new lowWatermark
    # and records that have a LogSequenceNumber lower can be forgotten

    for record in journal:
        if record.getOperation() == "Begin" and record.getTransactionID() not in committed:
            assert lowWatermark == -1
            lowWatermark = record.getLogSequenceNumber()
            break

    # resetting the committed set
    committed = set()


    # We read all the records
    # First we store in two different sets all the transactionIDs
    # of transactions that have
    # a commit record and a prepare record in the journal 
    # that have not been checkpointed yet

    for record in journal:
        if  (
            record.getType() == "System" 
        and (record.getOperation() == "Prepared" or record.getOperation() == "Abort")
        # Non inferieur
        and not record.getDependency() < checkpointTime
            ):
            assert not record.getTransactionID() in prepared
            prepared.add(record.getTransactionID())
            assert record.getTransactionID() in prepared
        elif(
            record.getType() == "System" 
        and (record.getOperation() == "Commit")
        and not record.getDependency() < checkpointTime
            ):
            assert not record.getTransactionID() in committed
            committed.add(record.getTransactionID())
            assert record.getTransactionID() in committed
        else:
            assert not (record.getType() == "System" and record.getOperation() == "Prepare")
            assert not (record.getType() == "System" and record.getOperation() == "Commit")
            assert not (record.getType() == "System" and record.getOperation() == "Abort")
            if (
                not record.getType() == "System"
            and not record.getDependency() < checkpointTime
            ):
                transactionIDs.add(record.getTransactionID())
                assert record.getTransactionID() in transactionIDs


    # Once we have a both sets we check if the commit list is a subset of prepare
    # And if the committed is a subset of transaction
    assert committed.issubset(prepared)
    assert prepared.issubset(transactionIDs)
    
    # We single out the transactions that have no commit record or or prepare record
    # For now we return the transactionIDs for the abort 
    # records to be written in the journal. 
    # We cannot write the records now because the journal is not initialized yet
    transactionsToAbort = transactionIDs.difference(prepared)
    # Should not be None
    assert not transactionsToAbort.issubset(committed)
    assert not transactionsToAbort.issubset(prepared)

    transactionsWithoutCommit = prepared.difference(committed)
    assert not transactionsToAbort.issubset(transactionsWithoutCommit)

    # This dict contains the key of transactions that are missing a commit message
    # And for each the list of participants
    trWithoutCommitAndParticipants = dict()

    for record in journal:
        if record.getOperation() == "Prepare" 
        and record.getTransactionID() in transactionsWithoutCommit:
            transactionID = record.getTransactionID()
            listOfParticipants = record.getParticipants
            trWithoutCommitAndParticipants[tranactransactionID] = listOfParticipants
    
    return {lowWatermark, highWatermark, checkpointTime, 
    transactionsToAbort, trWithoutCommitAndParticipants}


