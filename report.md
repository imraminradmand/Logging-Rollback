<!-- From D2L:

Report: it should include your main "design decisions", like data structures, data formats, etc. You could include as well screen captures of your running-code covering the two transaction blocks, showing the status/values for database tables and Logging Sub-system. -->

# Report

## Team members

- Diego Anzola
- Ramin Radmand
- Emelie Obiagu

## General Overview

This script implements a financial transaction block that moves money from a checking account to a savings account for a given customer. It performs the following steps:

1. Instantiates three dataframes for customers, accounts and account balances.
2. Calls the function `transaction_block` with the input parameters of customer ID, amount of money, and a flag indicating whether the transaction should fail.
3. Within the `transaction_block`, it performs the following:
   1. Calculates a transaction ID based on the current date and time.
   2. Retrieves the customer's information, account numbers, and account balances.
   3. Subtracts the money from the checking account and adds it to the savings account.
   4. If the transaction is successful, it logs the transaction status and the final account balances.
   5. If the transaction fails, it logs the transaction status, performs a rollback on the transaction, and displays the table.

## Design decisions

**Main memory:** We are using pandas dataframes as our main memory. We are using dataframes because they are easy to work with and their structure is similar to that of a database table.

The databases are populated with the data from the `.csv` files proviced in the assignemnt.

All of the transactions done in the program are done on the dataframes. When the transactions are complete and the data is ready to be commited. The dataframes are then written back to the `.csv` files.

**Secondary memory:** Our secondary storage are `.csv` files that were provided for us in the beginning code for this assignment.

Once the information is commited. These `.csv` files are updated with the new information from the dataframes.

**Logging subsystem:** We are using a logging subsystem to keep track of the transactions that are being done.

There are 2 "logs" in the system:

- `current_block_log` (dictionary) - This is the log for the current block of transactions. This log is used to keep track of the transactions that are being done in the current block. This log is cleared after the block is commited.

- `log_list` (list of dictionaries) - This is a persistent log that keeps track of all of the transactions that have been done in the system. Once the current block is done, the information in the `current_block_log` is appended to the `log_list`.

Whenever a report is printed, the `log_list` is printed out, as we want to see all of the transactions that have been done in the system.
