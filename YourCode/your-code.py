import datetime
import os

from constant import ID
from df_helpers import instantiate_dataframes, print_dataframes
from helpers import color_print, color_print_log

# Setup relative paths
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Log Sub-system (Persistent, not cleared after each block)
log_list = []

# Instantiate the Dataframes
df_customers, df_accounts, df_account_balances = instantiate_dataframes()


def transaction_block(id: str, money: int, faliure: bool):
    # Create a list to log the current block
    # current_block_log = []
    current_block_log = {
        "status": "",
        "transaction_id": "",
        "attribute": "",
        "table": "",
        "image_before": {},
        "image_after": {},
        "timestamp": "",
        "user": "",
    }

    # Create timestamp
    timestamp = datetime.datetime.now()

    # Create Transaction ID (YYYYMMDDHHMMSS)
    transaction_id = f"{timestamp.year}{timestamp.month}{timestamp.day}{timestamp.hour}{timestamp.minute}{timestamp.second}"

    # Get the customer information of the id
    first_name = df_customers.loc[id, 'First Name']
    last_name = df_customers.loc[id, 'Last Name']

    # Get the account numbers of the id
    from_account = df_accounts.loc[id, 'Checking Account']
    to_account = df_accounts.loc[id, 'Saving Account']

    # Get the account balances of the account numbers
    from_account_balance = df_account_balances.loc[from_account, 'Balance']
    to_account_balance = df_account_balances.loc[to_account, 'Balance']

    df_temp = df_account_balances.copy()

    # Log the data onto the current block log
    # * BEFORE THE TRANSACTION
    current_block_log["transaction_id"] = transaction_id
    current_block_log["attribute"] = "Balance"
    current_block_log["table"] = "account-balance"
    current_block_log["image_before"] = df_temp
    current_block_log["timestamp"] = timestamp
    current_block_log["user"] = f"{first_name} {last_name}"

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

        current_block_log["status"] = "Failure"
        current_block_log["image_after"] = df_account_balances

        # Append the current block log to the log sub-system
        log_list.append(current_block_log)

        # Print the log sub-system
        color_print("Status of Log Sub-system:", "green")
        print_log()

        # TODO Auto rollback
        auto_rollback()

        # Reset the current block log
        current_block_log = {}
        return

    # Add money to the savings account
    color_print("Add money to another account.", "green")

    df_account_balances.loc[to_account, 'Balance'] = int(
        to_account_balance) + money

    print(
        f"Added ${money} to {first_name} {last_name}'s Savings Account ({to_account}).")

    # Log the data onto the current block log
    # * AFTER THE TRANSACTION
    current_block_log["status"] = "Success"
    current_block_log["image_after"] = df_account_balances

    # Append the current block log to the log sub-system
    log_list.append(current_block_log)

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
    current_block_log = {
        "status": "",
        "transaction_id": "",
        "attribute": "",
        "table": "",
        "image_before": {},
        "image_after": {},
        "timestamp": "",
        "user": "",
    }


def auto_rollback():
    ''' If a transaaction fails, the tables are updated to their last healthy state'''
    color_print("AUTO ROLLBACK INITIATED", "purple_1b")

    # Getting the last log
    log = log_list[-1]
    previous_image = log["image_before"]

    # Commiting the fix
    previous_image.to_csv(
        '../Data-Assignment-1/csv/account-balance.csv', header=False)

    color_print("AUTO ROLLBACK COMPLETED", "purple_1b")

    color_print_log("DB STATE AFTER ROLLBACK \n", "purple_1b", previous_image)


def print_log():

    if len(log_list) == 0:
        print("Log Sub-system is empty.")

    for log in log_list:
        color_print_log("Transaction ID:", "orange_1", log['transaction_id'])
        color_print_log("Status:", "orange_1", log['status'])
        color_print_log("Attribute:", "orange_1", log['attribute'])
        color_print_log("Table:", "orange_1", log['table'])
        color_print("Image Before:", "orange_1")
        print(log['image_before'])
        color_print("Image After:", "orange_1")
        print(log['image_after'])
        color_print_log("Timestamp:", "orange_1", log['timestamp'])
        color_print_log("User:", "orange_1", log['user'])
        print("-" * 50)


def main():
    color_print("First Output:", 'blue')

    color_print("Original Contents of Databases:", 'blue')
    print_dataframes(df_customers, df_accounts, df_account_balances)

    color_print("Original Contents of Log Sub-system:", 'blue')
    print_log()

    color_print("BLOCK TRANSACTION 1", 'green')
    transaction_block(ID, 100000, False)

    color_print("BLOCK TRANSACTION 2", 'green')
    transaction_block(ID, 100000, True)


if __name__ == "__main__":
    main()
