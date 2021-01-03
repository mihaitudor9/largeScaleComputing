import json
import socket

# a class representing the bank that gets client's commands from the main server


# read the configuration file
def reading(file):
    my_config_file1 = open(file)
    my_config_file1 = my_config_file1.read()
    object1 = json.loads(my_config_file1)
    return object1


# read bank's configuration
bank_data = reading('data/bank_config.json')

# try opening bank's log file, if it doesn't exist yet - create one (storing all the actions)
try:
    log = reading('data/bank_log.json')
except:
    log = {}
    log['money transfer'] = []
    log['money disbursal'] = []

# get the name and id
name = bank_data['login']['name']
idx = bank_data['login']['id']
print("Name:", name)
print("ID:", idx)
print("-----------------")

# get main server's ip and port
host = bank_data['server']['ip']
port = int(bank_data['server']['port'])


# a function that performs a given action
def perform_transaction(action):

    # read the action
    substr2 = action.split(']')
    transaction_type = substr2[1].split('[')[0]

    # read transaction's id and the sender's account number
    substr = action.split('[')
    transaction_id = substr[1].split(']')[0]
    fromAccount = substr[2].split(']')[0]

    foundAccount1 = False
    foundAccount2 = False

    # check if it's a money transfer
    if transaction_type == ' ADD ':
        # read the receiver account number and the amount to be sent
        toAccount = substr[3].split(']')[0]
        amount = substr[4].split(']')[0]

        for account in bank_data['accounts']:
            # update balance of fromAccount
            if fromAccount == account['number']:
                # if not enough balance then send the error to the client
                if float(account['balance']) < float(amount):
                    toreturn = str(transaction_id) + '#' + str('Error: balance too small')
                    return toreturn
                # otherwise update the account balance
                else:
                    account['balance'] = float(account['balance']) - float(amount)
                    foundAccount1 = True

            # update balance of toAccount
            if toAccount == account['holder'] or toAccount == account['number']:
                account['balance'] = float(account['balance']) + float(amount)
                foundAccount2 = True

        # if any of the accounts numbers are not found, send the errors
        if not foundAccount1:
            toreturn = str(transaction_id) + '#' + str('Error: sender account not found')
            return toreturn
        if not foundAccount2:
            toreturn = str(transaction_id) + '#' + str('Error: recipient account not found')
            return toreturn
        with open('data/bank_config.json', 'w') as outfile:
            json.dump(bank_data, outfile, indent=4)

        # save the transaction to the log file
        log['money transfer'].append({'from': fromAccount, 'to': toAccount, 'amount': amount})
        with open('data/bank_log.json', 'w') as outfile:
            json.dump(log, outfile)

        # transaction successful
        toreturn = str(transaction_id) + '#' + str('Transaction successful')
        return toreturn

    # check if it's disbursal of money
    elif transaction_type == ' SUB ':
        # read the amount to be disbursed
        amount = substr[3].split(']')[0]

        for account in bank_data['accounts']:
            # update balance of fromAccount
            if fromAccount == account['number']:
                # if not enough balance then send the error to the client
                if float(account['balance']) < float(amount):
                    toreturn = str(transaction_id) + '#' + str('Error: balance too small')
                    return toreturn
                # otherwise update the account balance
                else:
                    account['balance'] = float(account['balance']) - float(amount)
                    foundAccount1 = True

            # if the account number is not found, send the error
            if not foundAccount1:
                toreturn = str(transaction_id) + '#' + str('Error: sender account not found')
                return toreturn

        with open('data/bank_config.json', 'w') as outfile:
            json.dump(bank_data, outfile, indent=4)

        # save the transaction to the log file
        log['money disbursal'].append({'from': fromAccount, 'amount': amount})
        with open('data/bank_log.json', 'w') as outfile:
            json.dump(log, outfile)

        # transaction successful
        toreturn = str(transaction_id) + '#' + str('Transaction successful')
        return toreturn

    # the action doesn't exist
    else:
        toreturn = str(transaction_id) + '#' + str('Error: incorrect command')
        return toreturn


# open a socket connection
ClientSocket = socket.socket()

print('Waiting for connection')
# try connecting to the main server, otherwise print the error
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

# receive and print the welcome message
Welcome = ClientSocket.recv(1024)
print(Welcome.decode('utf-8'))

# register
registration_string = str(idx) + '#' + str(name)
ClientSocket.send(str.encode(registration_string))
Result = ClientSocket.recv(1024)
print(Result.decode('utf-8'))

# listen for transactions
while True:
    command = ClientSocket.recv(1024).decode('utf-8')
    print(command)
    response = perform_transaction(command)
    print(response)
    ClientSocket.send(str.encode(response))
