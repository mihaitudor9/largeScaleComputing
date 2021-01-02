import json
import socket
import time

def reading(file):
    my_config_file1 = open(file)
    my_config_file1 = my_config_file1.read()
    object1 = json.loads(my_config_file1)
    return object1

bank_data = reading('data/bank_config.json')

try:
    log = reading('data/bank_log.json')
except:
    log = {}
    log['money transfer'] = []
    log['money disbursal'] = []

name = bank_data['login']['name']
idx = bank_data['login']['id']
print("Name:", name)
print("ID:", idx)
print("-----------------")

host = bank_data['server']['ip']
port = int(bank_data['server']['port'])

def perform_transaction(action):
    
    substr2 = action.split(']')
    transaction_type = substr2[1].split('[')[0]

    substr = action.split('[')
    transaction_id = substr[1].split(']')[0]
    fromAccount = substr[2].split(']')[0]

    foundAccount1 = False
    foundAccount2 = False

    if transaction_type == ' ADD ':  # money transfer
        toAccount = substr[3].split(']')[0]
        amount = substr[4].split(']')[0]

        for account in bank_data['accounts']:
            #update balance of fromAccount
            if fromAccount == account['number']:
                if float(account['balance']) < float(amount):
                    toreturn = str(transaction_id) + '#' + str('Error: balance too small')
                    return toreturn
                else:
                    account['balance'] = float(account['balance']) - float(amount)
                    foundAccount1 = True

            #update balance of toAccount
            if toAccount == account['holder'] or toAccount == account['number']:
                account['balance'] = float(account['balance']) + float(amount)
                foundAccount2 = True

        if not foundAccount1:
            toreturn = str(transaction_id) + '#' + str('Error: sender account not found')
            return toreturn
        if not foundAccount2:
            toreturn = str(transaction_id) + '#' + str('Error: recipient account not found')
            return toreturn

        with open('data/bank_config.json', 'w') as outfile:
            json.dump(bank_data, outfile, indent=4)

        #log transaction
        log['money transfer'].append({'from': fromAccount, 'to': toAccount, 'amount': amount})
        with open('data/bank_log.json', 'w') as outfile:
            json.dump(log, outfile)

        toreturn = str(transaction_id) + '#' + str('Transaction successful')
        return toreturn

    elif transaction_type == ' SUB ':  # disbursal of money
        amount = substr[3].split(']')[0]

        for account in bank_data['accounts']:
            #update balance of fromAccount
            if fromAccount == account['number']:
                if float(account['balance']) < float(amount):
                    toreturn = str(transaction_id) + '#' + str('Error: balance too small')
                    return toreturn
                else:
                    account['balance'] = float(account['balance']) - float(amount)
                    foundAccount1 = True

            if not foundAccount1:
                toreturn = str(transaction_id) + '#' + str('Error: sender account not found')
                return toreturn

        with open('data/bank_config.json', 'w') as outfile:
            json.dump(bank_data, outfile, indent=4)

        #log transaction
        log['money disbursal'].append({'from': fromAccount, 'amount': amount})
        with open('data/bank_log.json', 'w') as outfile:
            json.dump(log, outfile)

        toreturn = str(transaction_id) + '#' + str('Transaction successful')
        return toreturn

    else:
        toreturn = str(transaction_id) + '#' + str('Error: incorrect command')
        return toreturn
    
ClientSocket = socket.socket()

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

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
