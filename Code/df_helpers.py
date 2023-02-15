import pandas as pd
from colored import attr, fg
from helpers import myreader


def instantiate_dataframes():
    """ Populate Dataframes with data from csv files (../Data-Assignment-1/) """

    customers = {
        "ID": [],
        "Last Name": [],
        "First Name": [],
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
        "Account Number": [],
        "Balance": [],
    }

    # Create a list for each csv file
    customer_list = myreader('../Data-Assignment-1/customer.csv')
    account_list = myreader('../Data-Assignment-1/account.csv')
    account_balance_list = myreader(
        '../Data-Assignment-1/account-balance.csv')

    # Appending the lists to the Dataframes
    for line in customer_list:
        customers["ID"].append(line[0])
        customers["Last Name"].append(line[1])
        customers["First Name"].append(line[2])
        customers["Address"].append(line[3])
        customers["City"].append(line[4])
        customers["Age"].append(line[5])

    for line in account_list:
        accounts["ID"].append(line[0])
        accounts["Checking Account"].append(line[1])
        accounts["Saving Account"].append(line[2])

    for line in account_balance_list:
        account_balances["Account Number"].append(line[0])
        account_balances["Balance"].append(line[1])

    # Instantiate Dataframes
    df_customers = pd.DataFrame(customers)
    df_accounts = pd.DataFrame(accounts)
    df_account_balances = pd.DataFrame(account_balances)

    # Set the indexes of the Dataframes to the keys of the tables
    df_customers.set_index('ID', inplace=True)
    df_accounts.set_index('ID', inplace=True)
    df_account_balances.set_index('Account Number', inplace=True)

    return (df_customers, df_accounts, df_account_balances)


def print_dataframes(df_customers, df_accounts, df_account_balances):
    """ Print each dataframe """
    print(f'{fg("orange_1")}Customers Dataframe:{attr("reset")}' "\n",
          df_customers, "\n")
    print(f'{fg("orange_1")}Accounts Dataframe:{attr("reset")}' "\n",
          df_accounts, "\n")
    print(f'{fg("orange_1")}Account Balances Dataframe:{attr("reset")}' "\n",
          df_account_balances, "\n")
