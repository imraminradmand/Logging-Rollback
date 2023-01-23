# Your Code
import csv
import pandas as pd


def myreader(filename: str):
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        your_list = list(reader)

    return (your_list)


def populate_dataframes():
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
