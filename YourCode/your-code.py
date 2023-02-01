import datetime
import os

import pandas as pd
from colored import attr, fg
from constant import ID
from df_helpers import instantiate_dataframes, print_dataframes
from helpers import color_print

# Setup relative paths
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Log Sub-system (Persistent, not cleared after each block)
log = []

# Instantiate the Dataframes
df_customers, df_accounts, df_account_balances = instantiate_dataframes()


def transaction_block(id: str, money: int, faliure: bool):
    # Create a list to log the current block
    current_block_log = []

    # Create timestamp
    timestamp = datetime.datetime.now()

    # Create Transaction ID (YYYYMMDDHHMMSS)
    transaction_id = f"{timestamp.year}{timestamp.month}{timestamp.day}{timestamp.hour}{timestamp.minute}{timestamp.second}"

    # Log the data onto the current block log
    # * BEFORE THE TRANSACTION
    current_block_log.append(transaction_id)
    current_block_log.append('account_balance')
    current_block_log.append("Balance")
    current_block_log.append(df_account_balances)

    # Get the customer information of the id
    first_name = df_customers.loc[id, 'First Name']
    last_name = df_customers.loc[id, 'Last Name']

    # Get the account numbers of the id
    from_account = df_accounts.loc[id, 'Checking Account']
    to_account = df_accounts.loc[id, 'Saving Account']

    # Get the account balances of the account numbers
    from_account_balance = df_account_balances.loc[from_account, 'Balance']
    to_account_balance = df_account_balances.loc[to_account, 'Balance']

    # Print the transaction information
    print(f"{first_name} {last_name} will be moving ${money} from their checking account ({from_account}) to their Savings Account ({to_account}).")

    # TODO - Ask if we can leave like this since it asks for all tables
    print(f"Balances:")
    print(f"  Checking: {from_account_balance}")
    print(f"  Savings: {to_account_balance}")

    # Subtract money from the checking account
    color_print("Subtract money from one account.", "green")

    df_account_balances.loc[from_account, 'Balance'] = int(
        from_account_balance) - money

    print(
        f"Subtracted ${money} from {first_name} {last_name}'s Checking Account ({from_account}).")

    # Handle a transaction failure
    if (faliure == True):
        # Commit removal of money from the checking account
        df_account_balances.to_csv(
            '../Data-Assignment-1/csv/account-balance.csv', header=False)

        color_print("Failure Detected", "red")

        # Log the data onto the current block log
        # * ERROR DURING TRANSACTION
        current_block_log.append(df_account_balances)
        current_block_log.append('Failed')
        current_block_log.append(timestamp)
        current_block_log.append('Emma')

        # Append the current block log to the log sub-system
        log.append(current_block_log)

        # Print the log sub-system
        print_log()

        # TODO Auto rollback
        # auto_rollback()

        # Reset the current block log
        current_block_log = []
        return

    # Add money to the savings account
    color_print("Add money to another account.", "green")

    df_account_balances.loc[to_account, 'Balance'] = int(
        to_account_balance) + money

    print(
        f"Added ${money} to {first_name} {last_name}'s Savings Account ({to_account}).")

    # Log the data onto the current block log
    # * AFTER THE TRANSACTION
    current_block_log.append(df_account_balances)
    current_block_log.append('completed')
    current_block_log.append(timestamp)
    current_block_log.append('Emma')

    # Append the current block log to the log sub-system
    log.append(current_block_log)

    # Commit the changes
    color_print("COMMIT all your changes", "green")

    df_account_balances.to_csv(
        '../Data-Assignment-1/csv/account-balance.csv', header=False)

    print("Changes committed to account-balance.csv")

    # update the variables
    from_account_balance = df_account_balances.loc[from_account, 'Balance']
    to_account_balance = df_account_balances.loc[to_account, 'Balance']

    # Print the Dataframes
    color_print("Contents of Databases", "green")

    # TODO - Ask if we can leave like this since it asks for all tables
    print(f"Balances:")
    print(f"  Checking: {from_account_balance}")
    print(f"  Savings: {to_account_balance}")

    # Print the Log Sub-system
    color_print("Status of Log Sub-system:", "green")
    print_log()

    # Clear log
    # TODO clear log - crashing for some reason


"""
AUTO ROLLBACK + LOG STRUCTURE

initial (before anything happens) logs = []

in trans. 1 =>
trans1current_block_log = [id, table, attr, imgB, imgA, completed, timestamp, userID]

after trans.1 =>
add trans1current_block_log to logs
logs = [ [id, table, attr, imgB, imgA, status, timestamp, userID] ]

before trans.2 start =>
logs = [ [id, table, attr, imgB, imgA, status, timestamp, userID] ]

during trans. 2 =>
trans2current_block_log = [id2, table, attr, imgB, imgA, failed, timestamp, userID]

after trans2 =>
logs = [ [id, table, attr, imgB, imgA, status, timestamp, userID],  [id2, table, attr, imgB, imgA, failed, timestamp, userID] ]

look inside log for list that has status set to failed, grab that log, and then grab the before image from that log and use it for auto rollback

"""


def auto_rollback():
    print(f'{fg("green")}AUTO ROLLBACK INITIATED...{attr("reset")}')
    # Getting before image from the log and converting to df
    elem = [i for i in log if i[5] == 'Failed']
    # print(elem)
    previous_image = pd.DataFrame(elem[0][3])
    previous_image.set_index('Account Number', inplace=True)
    previous_image.to_csv(
        '../Data-Assignment-1/csv/account-balance.csv', header=False)
    print(f'{fg("green")}ROLLBACK COMPLETED{attr("reset")}')
    print(f'{fg("orange_1")}DB STATE AFTER ROLLBACK{attr("reset")}',
          "\n", previous_image)


def print_log():
    if len(log) == 0:
        print("Log Sub-system is empty", "\n")

    for i in range(len(log)):
        print(f'{fg("orange_1")}Transaction ID:{attr("reset")} {log[i][0]}',
              "\n", f'{fg("orange_1")}Table: {attr("reset")}{log[i][1]}',
              "\n", f'{fg("orange_1")}Attribute: {attr("reset")}{log[i][2]}', "\n",
              f'{fg("orange_1")}IMAGE BEFORE {attr("reset")}' "\n",
              f'{pd.DataFrame(log[i][3])}', "\n",
              f'{fg("orange_1")}IMAGE AFTER {attr("reset")}' "\n",
              f'{pd.DataFrame(log[i][4])}', "\n",
              f'{fg("orange_1")}Status: {attr("reset")}{log[i][5]}', "\n",
              f'{fg("orange_1")}Timestamp: {attr("reset")}{log[i][6]}', "\n",
              f'{fg("orange_1")}User: {attr("reset")}{log[i][7]}', "\n")
        print("---------------------------------------------------------")


def main():
    color_print("First Output:", 'blue')

    color_print("Original Contents of Databases:", 'blue')
    print_dataframes(df_customers, df_accounts, df_account_balances)

    color_print("Original Contents of Log Sub-system:", 'blue')
    print_log()

    color_print("BLOCK TRANSACTION 1", 'green')
    transaction_block(ID, 100000, False)

    # color_print("BLOCK TRANSACTION 2", 'green')
    # transaction_block(ID, 100000, True)


if __name__ == "__main__":
    main()
