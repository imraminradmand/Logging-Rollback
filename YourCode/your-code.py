# Your Code
import csv
import pandas as pd
from colored import fg, attr


def myreader(filename: str):
    """ Read csv file and return a list of lists """
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        your_list = list(reader)

    return (your_list)


def populate_dataframes():
    """ Populate Dataframes with data from csv files (../Data-Assignment-1/csv/) """
    # Populate Dataframes
    customer_list = myreader('../Data-Assignment-1/csv/customer.csv')
    account_list = myreader('../Data-Assignment-1/csv/account.csv')
    account_balance_list = myreader(
        '../Data-Assignment-1/csv/account-balance.csv')

    for line in customer_list:
        customers["ID"].append(line[0])
        customers["LastName"].append(line[1])
        customers["FirstName"].append(line[2])
        customers["Address"].append(line[3])
        customers["City"].append(line[4])
        customers["Age"].append(line[5])

    for line in account_list:
        accounts["ID"].append(line[0])
        accounts["Checking Account"].append(line[1])
        accounts["Saving Account"].append(line[2])

    for line in account_balance_list:
        account_balances["AccountNum"].append(line[0])
        account_balances["Balance"].append(line[1])


def print_dataframes():
    """ Print Dataframes """
    print("Customers Dataframe: \n \n", df_customers, "\n")
    print("Accounts Dataframe: \n \n", df_accounts, "\n")
    print("Account Balances Dataframe: \n \n", df_account_balances, "\n")


def transaction_block_1(id, money):
    """ Transaction Block 1: Successful """

    # Get the customer information of the id
    first_name = df_customers.loc[id, 'FirstName']
    last_name = df_customers.loc[id, 'LastName']

    # Get the account numbers of the id
    from_account = df_accounts.loc[id, 'Checking Account']
    to_account = df_accounts.loc[id, 'Saving Account']

    # Get the account balances of the account numbers
    from_account_balance = df_account_balances.loc[from_account, 'Balance']
    to_account_balance = df_account_balances.loc[to_account, 'Balance']

    print(f'{fg("green")}BLOCK TRANSACATION 1{attr("reset")}')

    # Print the transaction information
    print(f"{first_name} {last_name} will be moving ${money} from their checking account ({from_account}) to their Savings Account ({to_account}).")
    print("Balances:")
    print(f"  Checking: {from_account_balance}")
    print(f"  Savings: {to_account_balance}")

    # Subtract money from the checking account
    print(f'{fg("green")}Subtract money from one account.{attr("reset")}')

    df_account_balances.loc[from_account, 'Balance'] = int(
        from_account_balance) - money

    print(
        f"Subtracted ${money} from {first_name} {last_name}'s Checking Account ({from_account}).")

    # Add money to the savings account
    print(f'{fg("green")}Add money to second one{attr("reset")}')

    df_account_balances.loc[to_account, 'Balance'] = int(
        to_account_balance) + money

    print(
        f"Added ${money} to {first_name} {last_name}'s Savings Account ({to_account}).")

    # Commit the changes
    print(f'{fg("green")}COMMIT all your changes{attr("reset")}')

    df_account_balances.to_csv(
        '../Data-Assignment-1/csv/account-balance.csv')

    print("Changes committed to account-balance.csv")

    # Print the Dataframes
    # TODO for testing, currently only printing values, not whole Dataframes
    print(f'{fg("green")}Print Contents of Databases{attr("reset")}')

    # update the variables
    from_account_balance = df_account_balances.loc[from_account, 'Balance']
    to_account_balance = df_account_balances.loc[to_account, 'Balance']

    print("Balances:")
    print(f"  Checking: {from_account_balance}")
    print(f"  Savings: {to_account_balance}")

    # Print the Log Sub-system
    print(f'{fg("green")}Print current status of Log Sub-system{attr("reset")}')

    # TODO: Print the Log Sub-system


# Dataframe will hold data from customer.csv
customers = {
    "ID": [],
    "LastName": [],
    "FirstName": [],
    "Address": [],
    "City": [],
    "Age": [],
}

# Dataframe will hold data from account.csv
accounts = {
    "ID": [],
    "Checking Account": [],
    "Saving Account": [],
}

# Dataframe will hold data from account-balance.csv
account_balances = {
    "AccountNum": [],
    "Balance": [],
}

# Populate Dataframes
populate_dataframes()

# Instantiate Dataframes
df_customers = pd.DataFrame(customers)
df_accounts = pd.DataFrame(accounts)
df_account_balances = pd.DataFrame(account_balances)

# Set the indexes of the Dataframes to the keys of the tables
df_customers.set_index('ID', inplace=True)
df_accounts.set_index('ID', inplace=True)
df_account_balances.set_index('AccountNum', inplace=True)

# Print Dataframes
print_dataframes()

# This program only focuses on Emma Frost's account
id = "3"

transaction_block_1(id, 100000)
