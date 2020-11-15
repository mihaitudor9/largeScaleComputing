import json
import socket

#This client opens up a socket connection with the server, but only if the server program is currently running
def reading(file):
    my_config_file1 = open(file)
    my_config_file1 = my_config_file1.read()
    object1 = json.loads(my_config_file1)
    return object1
client1 = reading('/Users/wafaaaljbawi/Desktop/largeScaleComputing/data/config_1.json')
id = client1['person']['id']
firstname = client1['person']['name']
publickey = client1['person']['keys']['public']
#print("client 1 ID: " + id + " , Name:" + firstname + " , public key is: , " + publickey)

host =  client1['server']['ip']
port = int(client1['server']['port'])

ClientSocket = socket.socket()

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

Response = ClientSocket.recv(1024)
while True:
    Input = input('Say Something: ')
    ClientSocket.send(str.encode(Input))
    ClientSocket.send(str.encode(id))
    ClientSocket.send(str.encode(firstname))
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))

ClientSocket.close()