import json
import socket

#This client opens up a socket connection with the server, but only if the server program is currently running
def reading(file):
    my_config_file1 = open(file)
    my_config_file1 = my_config_file1.read()
    object1 = json.loads(my_config_file1)
    return object1
client1 = reading('data/config_1.json')
idx = client1['person']['id']
firstname = client1['person']['name']
publickey = client1['person']['keys']['public']
print("client 1 ID: " + idx + " , Name:" + firstname + " , public key is: , " + publickey)

host =  client1['server']['ip']
port = int(client1['server']['port'])

ClientSocket = socket.socket()

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

Welcome = ClientSocket.recv(1024)
print(Welcome.decode('utf-8'))

#register
ClientSocket.send(str.encode(idx))
ClientSocket.send(str.encode(firstname))
Result = ClientSocket.recv(1024)
print(Result.decode('utf-8'))

#send messages
while True:
    message = input('Enter message: ')
    ClientSocket.send(str.encode(message))
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))

ClientSocket.close()
