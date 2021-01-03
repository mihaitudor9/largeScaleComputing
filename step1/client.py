import json
import socket

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64


# This client class opens up a socket connection with the server, but only if the server program is currently running

# read a configuration file
def reading(file):
    my_config_file1 = open(file)
    my_config_file1 = my_config_file1.read()
    object1 = json.loads(my_config_file1)
    return object1


# store client data (for a different client choose a different file, i.e. config_2.json)
client_data = reading('data/config_1.json')
try:
    log = reading('..data/client_log.json')  # log file printing client's messages
except:
    log = {}
    log['sending'] = []  # sent messages
    log['receiving'] = []  # received messages
idx = client_data['person']['id']  # client's id
firstName = client_data['person']['name']  # client's first name
publicKey = client_data['person']['keys']['public']  # client's public key
print("Client 1 ID: ", idx)  # print client's details
print("Name:", firstName)
print("Public key:", publicKey)
print("-----------------")

host = client_data['server']['ip']  # server ip
port = int(client_data['server']['port'])  # server port


# a function that encrypts a message given the key
def encrypt(message, key):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(key)
    key_ready = Fernet(base64.urlsafe_b64encode(digest.finalize()))

    message = message.encode('utf-8')
    return key_ready.encrypt(message)


# a function that decrypts a message
def decrypt(message):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(publicKey.encode())
    key_ready = Fernet(base64.urlsafe_b64encode(digest.finalize()))

    return key_ready.decrypt(message)


# create a socket connection
ClientSocket = socket.socket()

print('Waiting for connection')
# try connecting to the server, otherwise print the error
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

# receive and print the welcome message from the server
Welcome = ClientSocket.recv(1024)
print(Welcome.decode('utf-8'))

# register in the server (id, first name and public key)
ClientSocket.send(str.encode(idx))
ClientSocket.send(str.encode(firstName))
ClientSocket.send(str.encode(publicKey))
# send the number of actions
number = str(len(client_data['actions']))
ClientSocket.send(str.encode(number))
Result = ClientSocket.recv(1024)
print(Result.decode('utf-8'))


# a function that executes client's actions - sends messages
def sendMessages(client_data):
    for action in client_data['actions']:
        # send the recipient of the message to the server
        substr = action.split('[')
        address = substr[1].split(']')[0]
        ClientSocket.send(str.encode(address))

        # get public key
        key = ClientSocket.recv(1024)
        if key == 'not found':
            raise Exception('recipient not found')
        else:
            message = substr[2].split(']')[0]
            print('sending', message, 'to', address)
            # save the message in the log file
            log['sending'].append({'from': firstName, 'to': address, 'message': str(message)})
            with open('data/client_log.json', 'w') as outfile:
                json.dump(log, outfile)

            # encrypt message and send the message
            encrypted = encrypt(message, key)
            ClientSocket.send(str.encode(str(encrypted)))


# try sending the messages
# in case of en error the client can retry or end the connection
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
        # decrypt and print the incoming messages
        incoming = decrypt(ClientSocket.recv(1024))
        print(incoming)
        # save the incoming messages to the log file
        log['receiving'].append({'by': firstName, 'message': str(incoming)})
        with open('../data/client_log.json', 'w') as outfile:
            json.dump(log, outfile)
    except:
        print('no incoming messages')

# close the connection
ClientSocket.close()