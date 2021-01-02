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

name = client_data['login']['name']
idx = client_data['login']['id']
print("Name:", name)
print("ID:", idx)
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
number = str(len(client_data['actions']))
registration_string = str(idx) + '#' + str(name) + '#' + str(accountNumber) + '#' + number
ClientSocket.send(str.encode(registration_string))
Result = ClientSocket.recv(1024)
print(Result.decode('utf-8'))

#perform transactions

#In while loop, listen for incoming commands from server, 
#and for each command, interpret it (split string, get account numbers and amount)
#and perform the command by editing the balance in bank_config.json for correct accounts
#then send response to server if transaction was successful or not
