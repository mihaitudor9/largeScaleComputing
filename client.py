import json
import socket

import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

#This client opens up a socket connection with the server, but only if the server program is currently running
def reading(file):
    my_config_file1 = open(file)
    my_config_file1 = my_config_file1.read()
    object1 = json.loads(my_config_file1)
    return object1


client_data = reading('data/config_1.json')
try:
    log = reading('data/client_log.json')
except:
    log = {}
    log['sending'] = []
    log['receiving'] = []
idx = client_data['person']['id']
firstName = client_data['person']['name']
publicKey = client_data['person']['keys']['public']
print("Client 1 ID: ", idx)
print("Name:", firstName)
print("Public key:", publicKey)
print("-----------------")

host = client_data['server']['ip']
port = int(client_data['server']['port'])

def encrypt(message, key):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(key)
    key_ready = Fernet(base64.urlsafe_b64encode(digest.finalize()))
    
    message = message.encode('utf-8')
    return key_ready.encrypt(message)

def decrypt(message):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(publicKey.encode())
    key_ready = Fernet(base64.urlsafe_b64encode(digest.finalize()))
    
    return key_ready.decrypt(message)


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
ClientSocket.send(str.encode(publicKey))
number = str(len(client_data['actions']))
ClientSocket.send(str.encode(number))
Result = ClientSocket.recv(1024)
print(Result.decode('utf-8'))

# send messages
def sendMessages(client_data):
    for action in client_data['actions']:
        substr = action.split('[')
        adres = substr[1].split(']')[0]
        #get public key
        ClientSocket.send(str.encode(adres))
    
        key = ClientSocket.recv(1024)
        if key == 'not found':
            raise Exception('recipient not found')
        else:
            #encrypt message
            message = substr[2].split(']')[0]
            print('sending', message, 'to', adres)
            #log message
            log['sending'].append({'from': firstName, 'to': adres, 'message': str(message)})
            with open('data/client_log.json', 'w') as outfile:
                json.dump(log, outfile)
            
            encrypted = encrypt(message, key)
            #send message
            ClientSocket.send(str.encode(str(encrypted)))

try:
    sendMessages(client_data)
    print('Messages sent.')
except socket.error as e:
    print('Error: ' + str(e))
    response = 'Messages not sent. Do you want to retry again?'
    ans = input(response)
    if ans == 'yes':
        sendMessages(client_data)

# listen for incoming messages
while True:
    try:
        incoming = decrypt(ClientSocket.recv(1024))
        print(incoming)
        #log message
        log['receiving'].append({'by': firstName, 'message': str(incoming)})
        with open('data/client_log.json', 'w') as outfile:
            json.dump(log, outfile)
    except:
        print('no incoming messages')

ClientSocket.close()
