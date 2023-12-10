import csv, time, subprocess, requests, os
from datetime import datetime

base_url = "https://api.etherscan.io/api?module=account&action=tokentx&"
contract_adress = ""
wallet_adress = "address="
transactions_list = []
api_key = "&apikey=XUA2BS48N6Z8X1C9XY3Q99RGI96MQYK3JG"
VALUE_FORMAT = '{:,.4f}'

def transaction_mode(wallet_checker, from_address):
    if wallet_checker == from_address:
        return "Transaction Mode: OUTGOING"
    else:
        return "Transaction Mode: INCOMING"

starter_page = int(input("\033[93m------ Wallet Checker ------\n\n\033[0m1. Token Transfer Events by Wallet\n2. Token Transfer Events by List of Wallets\n3. Exit\n\n\033[0m[?] Enter number: "))
if starter_page == 3:
    exit()
elif starter_page == 1 or starter_page == 2:
    os.system('clear')

    if starter_page == 1:
        form_wallet = input("---> Get a list of '\033[93mERC20 - Token Transfer Events' by Address\033[90m <---\n\n1. Please enter the target \033[93mWallet Address\033[90m: ")
        wallet_adress += form_wallet
        print(f"\033[32mInformation: {base_url}{wallet_adress}{api_key}")
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
        file_path = "/root/testing/wallets/" + search_term + ".txt"
        with open(file_path, mode='w') as filee:
            for ind in founded:
                filee.write(transactions_list[ind] + "\n")
        print("Process Completed.")
        subprocess.run(['xdg-open', file_path]) 

    elif option_item == 2:
        os.system('clear')
        file_path = "/root/testing/wallets/" + form_wallet + ".txt"
        with open(file_path, 'w+', encoding='utf-8') as filee:
            for value in transactions_list:
                filee.write(str(value) + "\n")
            filee.write("Found " + str(len(transactions_list)) + " Transactions.")
        print("\033[32mFile Exported: "+ file_path +"\033[0m")
        subprocess.run(['xdg-open', file_path])

        
    if starter_page == 2:
        os.system('clear')
        file_path = input("---> Get a list of 'ERC20 - Token Transfer Events' by Addresses <---\n\n1. Please enter the file path containing wallet addresses: ")
        print("\033[93mProcessing Started...\033[0m")
        start_time = time.time()

    all_transactions = {}

    with open(file_path, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)
        wallets_column = header.index('Wallets')

        for value in csv_reader:
            wallet = value[wallets_column]
            response = requests.get(base_url + wallet_adress + wallet + api_key)

            if response.status_code == 200:
                data = response.json()
                response_result = data.get('result', [])
                transactions_list = []

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

                # Use the same name for the dictionary as in the previous code
                all_transactions[wallet] = transactions_list

                total_transactions = len(transactions_list)

                file_path_wallet = f"/root/testing/wallets/{wallet}.txt"
                with open(file_path_wallet, 'w+', encoding='utf-8') as filee:
                    for entry in transactions_list:
                        filee.write(str(entry) + "\n")
                    filee.write(f"Found {total_transactions} Transactions.")

            else:
                print(f"Can't fetching data for {wallet}: {response.status_code}")
    end_time = time.time()
    os.system('clear')
    processing_time = (end_time - start_time) / 60
    option_item = int(input(
        "------ Implementation Completed ------\n--->" +
        "\033[32m" + f'{sum(len(transactions) for transactions in all_transactions.values()):,.4f}' +
        f" Transactions Collected. <---\n\033[93mProcessing Time: {processing_time} seconds\033[0m\n\n\033[0m1. Search your term in Transactions\n2. Export Transactions\n\n[?] Enter Number: "
    ))

    if option_item == 1:
        founded = []
        os.system('clear')
        search_term = str(input("Enter the search term: ")).lower()
        result_file_path = f"/root/testing/search_results_{search_term}.txt"

        with open(result_file_path, 'w', encoding='utf-8') as result_file:
            for wallet, transactions_list in all_transactions.items():
                for index, entry in enumerate(transactions_list):
                    if search_term in entry.lower():
                        founded.append((wallet, index))
                        result_file.write(transactions_list[index] + "\n")
                        result_file.write(entry + "\n")  # Use 'entry' directly
                        result_file.write("------\n")

            print(f"Results written to: {result_file_path}")
            subprocess.run(['xdg-open', result_file_path])

    elif option_item == 2:
        print("\033[32mFiles Exported:\033[0m")
        for wallet in all_transactions.keys():
            print(f"/root/testing/wallets/{wallet}.txt")

        merged_file_path = "/root/testing/Wallet/transactions_wallets.txt"
        with open(merged_file_path, 'w+', encoding='utf-8') as merged_file:
            for wallet, transactions_list in all_transactions.items():
                merged_file.write(f"Transactions for wallet {wallet}:\n")
                for entry in transactions_list:
                    merged_file.write(str(entry) + "\n")
                merged_file.write(f"Found {len(transactions_list)} Transactions.\n")
            print("\033[32mFile Exported: " + merged_file_path + "\033[0m")
            subprocess.run(['xdg-open', merged_file_path])
