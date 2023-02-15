<!-- From D2L:

Report: it should include your main "design decisions'', like data structures, data formats, etc. You could include screen captures of your running-code covering the two transaction blocks, showing the status/values for database tables and Logging Subsystem. -->

# Report

## Team members

- Diego Anzola
- Ramin Radmand
- Emelie Obiagu

## General Overview

This script implements a financial transaction block that moves money from a checking account to a savings account for a given customer. It performs the following steps:

1. Instantiates three dataframes (tables) for customers, accounts, and account balances.
2. Call the function `transaction_block` with the input parameters of customer ID, amount of money, and a flag indicating whether the transaction should fail.
3. Within the `transaction_block`, it performs the following:
   1. Calculates a transaction ID based on the current date and time.
   2. Retrieves the customer's information, including the account numbers and balances.
   3. Subtracts the money from the checking account and adds it to the savings account.
   4. If the transaction is successful, it logs the successful transaction into the log.
   5. If the transaction fails, it logs the unsuccessful transaction into the log, and performs a rollback on the transaction.

## Design decisions

**Main memory:** We are using pandas dataframes as our main memory. We are using dataframes because they are easy to work with and their structure is similar to that of a database table.

The databases are populated with the data from the `.csv` files provided in the assignment.

All of the transactions done in the program are done on the dataframes. When the transactions are complete and the data is ready to be committed, the dataframes are then written back to the `.csv` files (secondary memory).

**Secondary memory:** Our secondary storage are the `.csv` files that were provided for us in the starter code for this assignment.

Once the information is committed. These `.csv` files are updated with the new information from the dataframes.

**Logging subsystem:** We are using a logging subsystem to keep track of the transactions that are being done.

There are 2 "logs" in the system:

- `current_block_log` (dictionary) - This is the log for the current transaction block. This log is used to keep track of the transactions that are being done in the current block. Once the transactions are complete (subtracting from checking and adding to savings), the information in this log is appended to the `log_list`. This log is cleared after the block is committed.

  - Structure of the `current_block_log`:

    ```python
    current_block_log = {
       "status": "",           #"success" or "failure"
       "transaction_id": "",   # transaction ID
       "attribute": "",        # name of the attribute that was changed (e.g. "balance")
       "table": "",            # name of the table that was changed (e.g. "accounts")
       "image_before": {},     # content of the table before the change
       "image_after": {},      # content of the table after the change
       "timestamp": "",        # timestamp of the transaction
       "user": "",             # user that performed the transaction
    }
    ```

- `log_list` (list of dictionaries) - This is a persistent log that keeps track of all of the transactions that have been done in the system. Once the current block is done, the information in the `current_block_log` is appended to the `log_list`. Whenever a report is printed, the `log_list` is printed out, as we want to see all of the transactions that have been done in the system.

---

## Notes From Team After Completing the Assignment:

- After talking to our professor, we realized that instead of having the whole table in the `image_before` and `image_after` fields, we should only have the row that was changed. Since if the table is large, it would be a lot of data to store in the log.
