import json
import socket

import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64


# This client opens up a socket connection with the server, but only if the server program is currently running
def reading(file):
    my_config_file1 = open(file)
    my_config_file1 = my_config_file1.read()
    object1 = json.loads(my_config_file1)
    return object1


client_data = reading('data/bank_config_1')
try:
    log = reading('data/bankclient_log.json')
except:
    log = {}
    log['money transfer'] = []
    log['money disbursal'] = []
idx = client_data['person']['id']
firstName = client_data['person']['name']
accountNumber = client_data['account']['number']
balance = client_data['account']['savings']
print("Client 1 ID: ", idx)
print("Name:", firstName)
print("Account number:", accountNumber)
print("Current balance: ", balance)
print("-----------------")

host = client_data['server']['ip']
port = int(client_data['server']['port'])

ClientSocket = socket.socket()

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

Welcome = ClientSocket.recv(1024)
print(Welcome.decode('utf-8'))

# register
ClientSocket.send(str.encode(idx))
ClientSocket.send(str.encode(firstName))
ClientSocket.send(str.encode(accountNumber))
ClientSocket.send(str.encode(balance))
number = str(len(client_data['actions']))
ClientSocket.send(str.encode(number))
Result = ClientSocket.recv(1024)
print(Result.decode('utf-8'))


def bankingActions(client_data):
    for actions in client_data['actions']:
        substr2 = actions.split(']')
        action = substr2[1].split('[')[0]
        ClientSocket.send(str.encode(action))

        substr = actions.split('[')
        address = substr[1].split(']')[0]
        fromAccount = substr[2].split(']')[0]
        ClientSocket.send(str.encode(address))
        ClientSocket.send(str.encode(fromAccount))

        if action == ' ADD ':  # money transfer
            toAccount = substr[3].split(']')[0]
            amount = substr[4].split(']')[0]
            if int(amount) > int(balance):
                print('Failed to send money. Not enough balance')
            else:
                ClientSocket.send(str.encode(toAccount))
                ClientSocket.send(str.encode(amount))
                print('sending', amount, 'from account number', fromAccount, 'to account number', toAccount)
                # log message
                log['money transfer'].append({'from': fromAccount, 'to': toAccount, 'amount': amount})
                with open('data/bankclient_log.json', 'w') as outfile:
                    json.dump(log, outfile)
        elif action == ' SUB ':  # disbursal of money
            amount = substr[3].split(']')[0]
            if int(amount) > int(balance):
                print('Failed to disburse money. Not enough balance')
            else:
                ClientSocket.send(str.encode(amount))
                print('disbursal of', amount, 'from account number', fromAccount)
                # log message
                log['money disbursal'].append({'from': fromAccount, 'amount': amount})
                with open('data/bankclient_log.json', 'w') as outfile:
                    json.dump(log, outfile)
        else:
            print('no such action')


try:
    bankingActions(client_data)
    print('Actions finished.')
except socket.error as e:
    print('Error: ' + str(e))
    response = 'Do you want to retry again?'
    ans = input(response)
    if ans == 'yes':
        bankingActions(client_data)


ClientSocket.close()
