# Truncation is done sequentially
# Explain the problem
# Problem: When we want to truncate the log we need to ensure
# that no information is lost while checkpointing
#


def truncate(journal):

    # Retrieve the last checkpoint time
    checkpointTime = lastCheckpoint().getTimestamp()

    # committed is a list of all the transaction that have a prepare message
    # in the log
    committed = {}

    # This loop reads all the records in the journal and save the transactionID
    # of all the transactions that have a prepare message preceding the last
    # checkpoint

    for record in journal:
        if record.getTimestamp() < checkpointTime:
            # Je suppose que nous ne sommes pas en recovery
            # donc toutes les transactions terminées sont complètes
            if record.getType() == "System" and record.getOperation() == "Commit":
                committed.add(record.getTransactionID())
        else:
            # record.getTimestamp() >= checkpointTime
            break

    # We now have all the transactionIDs of terminated transactions

    # We read the log a second time and find the first record that has a
    # transactionID that is not present in committed is the new lowWatermark
    # and records that have a LSN lower can be forgotten

    for record in journal:
        if record.getTransactionID() not in committed:
            lowWatermark = record.getlogSequenceNumber()
            break

    # Assert New lowWatermark >= old lowWatermark
