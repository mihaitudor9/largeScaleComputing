import socket
import json
from _thread import *
import requests

def reading(file):
    my_config_file1 = open(file)
    my_config_file1 = my_config_file1.read()
    object1 = json.loads(my_config_file1)
    return object1


credentials = reading('data/credentials.json')
messages = []
try:
    log = reading('data/server_log.json')
except:
    log = {}
    log['messages'] = []
keys = [["6398C613619E4DCA88220ACA49603D87","EIFERT, THOMAS","MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAuD0NCJ9GVK1XrfcJkiDsKoYRt0qf0/ZF5UO8STki6Paez+haUhp3u0ce2IxpML7uHi8x4TakytWtVG2688WBWtX3YduMf9tCydWg79T++yb8md/P2Po9xy5JE9QNpYVEuChGvzQ2soGnXVo+7aIzrUHkSfZHRzDQGj6k3l2i5ifqF8o8FBJqJIfbOAr+HTkKrYbm7cWJ+f/WRcd3VkPUx/JxbZtDHE2VlCLgOO5RcovA75C8lbiHZZ3rpw1RyV0CwWSJUuiUxDvGZcQwTI55tSDEtTnRQeIWBxBPTEpu1JymF9E2A4bMkFnp02y6CnmSJ4oevhx18QYorNT4GNZv/xz02KVkZ3SWQacDnZu2iM9boq+7JGNH4R0paJFp/RZXNhhPXf1LHUmf5eIgk7MDH5cVaE7wWd6S0425v6kaQK9cDM5GpM80hdzVM8fQE7U0YOl1zphvR5+VQ2+pi0AGwzHJaA2PayKQFUEMlR2wTJIelW28gWgFRkp8FCzT+6PZoJEYgs4o6JwzQC9ax1aofLcepOgP4ILkS/jjeT1QtHkETOTt53c8umE/xb4mk/u4n3NZ4WosK2GNxbwHgrOzYKPwyDTeBnFIj27WR4LlaahqA+0U3MUk2ifqHh6NTCAwNXNCwmpSC8uLK3Q0ypwLlzNuppzk3snKH6/1BpEVHq0CAwEAAQ=="]]

# a function that handles requests from the individual client by a thread
# threaded_client() connects to each individual client on the different address given by the server
def threaded_client(connection):
    
    global idx, name
    global keys
    welcome = 'Welcome to the Server\n'
    connection.send(str.encode(welcome))
    registered = False

    # REGISTRATION
    try:
        idx = connection.recv(1024).decode('utf-8')
        name = connection.recv(1024).decode('utf-8')
        key = connection.recv(1024).decode('utf-8')
        keys.append([idx,name,key])
        number = connection.recv(1024).decode('utf-8')
    except:
        response = 'Registration error: incorrect format'
        connection.send(str.encode(response))
        connection.close()
        return False

    for user in credentials:
        if idx == user['user_ID'] and name == user['user_name']:
            response = 'Registration successful'
            connection.send(str.encode(response))
            registered = True
            break

    if not registered:
        response = 'Registration error: incorrect credentials'
        connection.send(str.encode(response))
        connection.close()
        return False

    
    #MESSAGING 
    global messages
    
    for i in range(int(number)):
        #check if recipient exists
        key_found = False
        adres = connection.recv(1024).decode('utf-8')
        print('Received adres:' + adres)
        for i in range(len(keys)):
            #send public key of recipient
            if keys[i][0] == adres or keys[i][1] == adres:
                key = str.encode(keys[i][2])
                connection.send(str.encode(keys[i][2]))
                key_found = True
        if not key_found:
            key = str.encode('not found')
            connection.send(str.encode('not found'))
        else:
            #send message - add message to public array
            message = connection.recv(1024)
            messages.append([adres, message])
            #add to logfile
            log['messages'].append({'from': name, 'to': adres, 'message': str(message)})
            with open('data/server_log.json', 'w') as outfile:
                json.dump(log, outfile)
            print('Received message:', message, 'to', adres)
        
    #Check for messages from other users
    for i in range(len(messages)):
        #iterate messages array and if ID or name match, send the message
        if messages[i][0] == idx or messages[i][0] == name:
            print("this matches, sending message")
            connection.send(messages[i][1])
            messages.remove(messages[i])

    return True

def server():
    ServerSocket = socket.socket()
    # declare host and port on which we need to communicate with clients
    ip = "127.0.0.1"
    print(ip)
    port = 13370
    ThreadCount = 0
    # if it binds successfully then it starts waiting for the client otherwise
    # it returns the error that occurred while establishing a connection
    try:
        ServerSocket.bind((ip, port))
    except socket.error as e:
        print(str(e))
    print('Waitiing for a Connection..')
    
    # use a while loop to make it run Server endlessly until we manually stop the Server
    while True:
        # accept connection from client using accept() function of socket server. It returns the type of client which
        # has connected and along with the unique thread number or address provided to it.
        ServerSocket.listen(5)
        Client, address = ServerSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        # Registration(id, firstname, publickey, ServerSocket, client1) use start_new_thread() function of thread
        # class which creates or assign a new thread to each client to handle them individually.
        start_new_thread(threaded_client, (Client,))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
    
    ServerSocket.close()



if __name__ == '__main__':
    server()
