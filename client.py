import base64
import json
import socket


# This client opens up a socket connection with the server, but only if the server program is currently running
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


def reading(file):
    my_config_file1 = open(file)
    my_config_file1 = my_config_file1.read()
    object1 = json.loads(my_config_file1)
    return object1


client1 = reading('data/config_1.json')
idx = client1['person']['id']
firstName = client1['person']['name']
publicKey = client1['person']['keys']['public']
print("Client 1 ID: ", idx)
print("Name:", firstName)
print("Public key:", publicKey)
print("-----------------")

host = client1['server']['ip']
port = int(client1['server']['port'])

def encrypt(message, key):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(key)
    key_ready = Fernet(base64.urlsafe_b64encode(digest.finalize()))
    
    message = message.encode('utf-8')
    return key_ready.encrypt(message)

def decrypt(message):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(publicKey)
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
        #encrypt message
        message = substr[2].split(']')[0]
        encrypted = encrypt(message, key)
        #send message
        ClientSocket.send(str.encode(adres))

try:
    sendMessages(client1)
    print('Messages sent.')
except socket.error as e:
    print('Error: ' + str(e))
    response = 'Messages not sent. Do you want to retry again?'
    ans = input(response)
    if ans == 'yes':
        sendMessages(client1)

# listen for incoming messages
while True:
    try:
        incoming = ClientSocket.recv(1024).decode('utf-8')
        # print(decrypt(incoming))
        print('you got a message:' + incoming)
    except:
        print('no incoming messages')


ClientSocket.close()
