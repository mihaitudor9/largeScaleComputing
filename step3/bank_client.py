import json
import socket
import time

def reading(file):
    my_config_file1 = open(file)
    my_config_file1 = my_config_file1.read()
    object1 = json.loads(my_config_file1)
    return object1

client_data = reading('data/bank_customer_1.json')
try:
    log = reading('data/bankclient_log.json')
except:
    log = {}
    log['transactions'] = []

name = client_data['person']['name']
idx = client_data['person']['id']
accountNumber = client_data['person']['account']
print("Name:", name)
print("ID:", idx)
print("Account number:", accountNumber)
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

# sending transactions
for action in client_data['actions']:
    ClientSocket.send(str.encode(action))
    print('sending:', action)
    
    log['transactions'].append({'transaction': action})
    with open('data/bankclient_log.json', 'w') as outfile:
        json.dump(log, outfile)
    time.sleep(1)
        
# listen for transaction status
while True:
    status = ClientSocket.recv(1024)
    print(status.decode('utf-8'))
