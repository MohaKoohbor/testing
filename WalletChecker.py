# Wallet Checker
import requests, os, subprocess, csv
from datetime import datetime
from colorama import Fore, Style

base_url = "https://api.etherscan.io/api?module=account&action=tokentx&"
contract_adress = ""
wallet_adress = "address="
transactions_list = []
api_key = "&apikey=XUA2BS48N6Z8X1C9XY3Q99RGI96MQYK3JG"
VALUE_FORMAT = '{:,.4f}'
# ----------------------------------------------------------- #

# -------------------- Def Section -------------------- #
def transaction_mode(wallet_checker, from_adress):
    if wallet_checker == from_adress:
        return "Transaction Mode: OUTGOING"
    else:
        return "Transaction Mode: INCOMING"
##########################################################
 # -------------------- End Section -------------------- #

starter_page = int(input("------ Basic Wallet Checker ------\n\n1. Token Transfer Events by Wallet\n2. Token Transfer Events by List of Wallets\n3. Exit\n\n[?] Enter number: "))
if starter_page == 3:
    exit()    
elif starter_page == 1:
    os.system('clear')
    form_wallet = input("---> Get a list of 'ERC20 - Token Transfer Events' by Address <---\n\n1. Please enter the target Wallet Address: ")
    wallet_adress += form_wallet
    print(f"Information: {base_url}{wallet_adress}{api_key}")
    
    response = requests.get(base_url+wallet_adress+api_key)
    
    if response.status_code == 200:
        data = response.json()
        response_result = data.get('result', [])
        transactions_list.clear()

        for result in response_result:
            time_stamp = result.get('timeStamp','N/A')
            hash = result.get('hash', 'N/A')
            from_adress = result.get('from', 'N/A')
            to_adress = result.get('to', 'N/A')
            token_symbol = result.get('tokenSymbol', 'N/A')
            token_name = result.get('tokenName', 'N/A')
            contract = result.get('contractAddress', 'N/A')
            value = result.get('value', 'N/A')
            value = float(value)/10**18
            valueStr = VALUE_FORMAT.format(value)
            timeStamp_utc = int(time_stamp)
            
            transactions_list.append(datetime.utcfromtimestamp(timeStamp_utc).strftime('%Y-%m-%d %H:%M:%S')+ " | Txn Hash: "+ hash +  
                                  "\n" + transaction_mode(form_wallet,from_adress) +"\nFrom: " + from_adress +
                                  f"\n[{token_symbol}] {token_name}: Contract: {contract}" + "\nTo: " + to_adress + "\nValue: " + valueStr + "\n-------")
    else:
        print(f"Can't fetching data: {response.status_code}")

    os.system('clear')
    option_item = int(input("------ Implementation Completed ------\n---> " + "\033[32m" + str(len(transactions_list)) +" Transactions Collected. <---\n\n\033[0m1. Search your term in Transactions\n2. Export Transactions\n\n[?] Enter Number: "))
    if option_item == 1:
        founded = []
        os.system('clear')
        search_term = str(input("Enter the search term: ")).lower()
        for index, entry in enumerate(transactions_list):
                 if search_term in entry.lower():
                    founded.append(index)
        file_path = "/root/testing/" + search_term + ".txt"
        with open(file_path, mode='w') as filee:
            for ind in founded:
                filee.write(transactions_list[ind] + "\n")
        print("Process Completed.")
        subprocess.run(['xdg-open', file_path]) 

    elif option_item == 2:
        os.system('clear')
        file_path = "/root/testing/" + form_wallet + ".txt"
        with open(file_path, 'w+', encoding='utf-8') as filee:
            for value in transactions_list:
                filee.write(str(value) + "\n")
            filee.write("Found " + str(len(transactions_list)) + " Transactions.")
        print("\033[32mFile Exported: "+ file_path +"\033[0m")
        subprocess.run(['xdg-open', file_path])

# ----------------- End Section of Menu 1 ----------------- #

# ... (Previous code)

elif starter_page == 2:
    os.system('clear')
    file_path = input("---> \033[93mGet a list of 'ERC20 - Token Transfer Events' by Addresses\033[0m <---\n\n1. Please enter the target Wallet Address: ")
    os.system('clear')
    
    with open(file_path, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)
        wallets_column = header.index('Wallets')
        wallets_list = []
        transactions_by_wallet = {}  # Use a dictionary to store transactions for each wallet

        for value in csv_reader:
            wallet = value[wallets_column]
            wallets_list.append(wallet)
            response = requests.get(base_url + wallet_adress + wallet + api_key)

            if response.status_code == 200:
                data = response.json()
                response_result = data.get('result', [])
                transactions_list = []  # Create a new list for each wallet

                for result in response_result:
                    time_stamp = result.get('timeStamp', 'N/A')
                    hash = result.get('hash', 'N/A')
                    from_address = result.get('from', 'N/A')
                    to_address = result.get('to', 'N/A')
                    token_symbol = result.get('tokenSymbol', 'N/A')
                    token_name = result.get('tokenName', 'N/A')
                    contract = result.get('contractAddress', 'N/A')
                    value = float(result.get('value', 0)) / 10**18
                    value_str = VALUE_FORMAT.format(value)
                    timeStamp_utc = int(time_stamp)
                    
                    transaction_entry = (
                        datetime.utcfromtimestamp(timeStamp_utc).strftime('%Y-%m-%d %H:%M:%S') +
                        " | Txn Hash: " + hash +
                        "\n" + transaction_mode(wallet, from_address) + "\nFrom: " + from_address +
                        f"\n[{token_symbol}] {token_name}: Contract: {contract}" + "\nTo: " + to_address + "\nValue: " + value_str + "\n-------"
                    )
                    transactions_list.append(transaction_entry)

                transactions_by_wallet[wallet] = transactions_list

                # Cache the total transactions count for each wallet
                total_transactions = len(transactions_list)
                
                # Write transactions to file
                file_path_wallet = f"E:\Wallet\\transactions_{wallet}.txt"
                with open(file_path_wallet, 'w+', encoding='utf-8') as filee:
                    for entry in transactions_list:
                        filee.write(str(entry) + "\n")
                    filee.write(f"Found {total_transactions} Transactions.")

            else:
                print(f"Can't fetching data for {wallet}: {response.status_code}")

        os.system('clear')
        option_item = int(input(
            "------ Implementation Completed ------\n---> " + 
            "\033[32m" + f'{sum(len(transactions) for transactions in transactions_by_wallet.values()):,.4f}' +
            " Transactions Collected. <---\n\n\033[0m1. Search your term in Transactions\n2. Export Transactions\n\n[?] Enter Number: "
        ))

        if option_item == 1:
        # Allow the user to search in transactions
            founded = []
            os.system('clear')
            search_term = str(input("Enter the search term: ")).lower()
            result_file_path = f"E:\\search_results_{search_term}.txt"

            with open(result_file_path, 'w', encoding='utf-8') as result_file:
                for wallet, transactions_list in transactions_by_wallet.items():
                    for index, entry in enumerate(transactions_list):
                        if search_term in entry.lower():
                            founded.append((wallet, index))
                            # Write the search result to the result file
                            result_file.write(f"Results in transactions of wallet {wallet}:\n")
                            result_file.write(transactions_by_wallet[wallet][index] + "\n")
                            result_file.write("------\n")

                print(f"Results written to: {result_file_path}")
                subprocess.run(['xdg-open', result_file_path])


        elif option_item == 2:
            # Inform the user about the location of exported files
            print("\033[32mFiles Exported:\033[0m")
            for wallet in wallets_list:
                print(f"E:\Wallet\\transactions_{wallet}.txt")

            # Open merged file with all transactions
            merged_file_path = "E:\Wallet\\transactions_wallets.txt"
            with open(merged_file_path, 'w+', encoding='utf-8') as merged_file:
                for wallet, transactions_list in transactions_by_wallet.items():
                    merged_file.write(f"Transactions for wallet {wallet}:\n")
                    for entry in transactions_list:
                        merged_file.write(str(entry) + "\n")
                    merged_file.write(f"Found {len(transactions_list)} Transactions.\n")
                print("\033[32mFile Exported: " + merged_file_path + "\033[0m")
                subprocess.run(['xdg-open', merged_file_path])
