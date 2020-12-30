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
commands = []
try:
    log = reading('data/serverbank_log.json')
except:
    log = {}
    log['money transfers'] = []
    log['money disbursals'] = []

# a function that handles requests from the individual client by a thread
# threaded_client() connects to each individual client on the different address given by the server
def threaded_client(connection):
    global idx, name
    welcome = 'Welcome to the Server\n'
    connection.send(str.encode(welcome))
    registered = False

    # REGISTRATION
    try:
        idx = connection.recv(1024).decode('utf-8')
        name = connection.recv(1024).decode('utf-8')
        accountNumber = connection.recv(1024).decode('utf-8')
        balance = connection.recv(1024).decode('utf-8')
        number = connection.recv(1024).decode('utf-8')
        print('number of actions', number)
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

    # MESSAGING
    global commands

    for i in range(int(number)):
        action = connection.recv(1024).decode('utf-8')
        address = connection.recv(1024).decode('utf-8')
        fromAccount = connection.recv(1024).decode('utf-8')
        print('Received action:' + action)
        print('Received address:' + address)
        print('Received fromaccount:' + fromAccount)
        if action == ' ADD ':  # money transfer
            # address = connection.recv(1024).decode('utf-8')
            # fromAccount = connection.recv(1024).decode('utf-8')
            toAccount = connection.recv(1024).decode('utf-8')
            print('received toaccount:', toAccount)
            amount = connection.recv(1024).decode('utf-8')
            print('received amount:', amount)
            commands.append([address, action, fromAccount, toAccount, amount])
            log['money transfers'].append({'from': fromAccount, 'to': toAccount, 'amount': amount})
            with open('data/serverbank_log.json', 'w') as outfile:
                json.dump(log, outfile)
            print('Received command: transfer from', fromAccount, 'to', toAccount, 'amount:', amount)
        elif action == ' SUB ':  # disbursal of money
            # address = connection.recv(1024).decode('utf-8')
            # fromAccount = connection.recv(1024).decode('utf-8')
            amount = connection.recv(1024).decode('utf-8')
            commands.append([address, action, fromAccount, amount])
            # add to logfile
            log['money disbursals'].append({'from': fromAccount, 'amount': amount})
            with open('data/serverbank_log.json', 'w') as outfile:
                json.dump(log, outfile)
            print('Received command: disbursal from', fromAccount, 'amount:', amount)
        else:
            print('no such action.')




    # Check for messages from other users
    for i in range(len(commands)):
        # iterate messages array and if ID or name match, send the message
        if commands[i][0] == idx or commands[i][0] == name:
            print("this matches, sending message")
            connection.send(commands[i][1])
            commands.remove(commands[i])

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
    print('Waiting for a Connection..')

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
