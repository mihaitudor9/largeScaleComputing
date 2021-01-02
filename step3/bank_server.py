import socket
import json
from _thread import *
import requests

def reading(file):
    my_config_file1 = open(file)
    my_config_file1 = my_config_file1.read()
    object1 = json.loads(my_config_file1)
    return object1
    
credentials = reading('data/bank_credentials.json')
transactions = []

try:
    log = reading('data/bankserver_log.json')
except:
    log = {}
    log['transactions'] = []
    
# a function that handles requests from the individual client by a thread
# threaded_client() connects to each individual client on the different address given by the server
def threaded_client(connection):
    welcome = 'Welcome to the Server\n'
    connection.send(str.encode(welcome))
    registered = False

    # REGISTRATION
    try:
        login_info = connection.recv(1024).decode('utf-8')
        print('login info:', login_info)
        client_id = login_info.split('#')[0]
        name = login_info.split('#')[1]
        accountNumber = login_info.split('#')[2]
        number = login_info.split('#')[3]
        
    except:
        response = 'Registration error: incorrect format'
        connection.send(str.encode(response))
        connection.close()
        return False

    for user in credentials:
        if name == user['user_name'] and client_id == user['user_id'] and accountNumber == user['account']:
            response = 'Registration successful'
            connection.send(str.encode(response))
            registered = True
            
    if not registered:
        response = 'Registration error: incorrect credentials'
        connection.send(str.encode(response))
        connection.close()
        return False

    # TRANSACTIONS
    global transactions

    for i in range(int(number)):
        action = connection.recv(1024).decode('utf-8')
        print('Received action:' + action)
        transactions.append(action)
        
        log['transactions'].append({'user': name, 'transaction': action})
        with open('data/serverbank_log.json', 'w') as outfile:
            json.dump(log, outfile)
    
    confirmation = 'The transaction requests have been sent to the bank!'
    connection.send(str.encode(confirmation))
    
    #connection.close()
    return True
    
def threaded_bank(connection):
    welcome = 'Welcome to the Server\n'
    connection.send(str.encode(welcome))
    registered = False

    # REGISTRATION
    try:
        login_info = connection.recv(1024).decode('utf-8')
        print('login info:', login_info)
        bank_id = login_info.split('#')[0]
        name = login_info.split('#')[1]
    except:
        response = 'Registration error: incorrect format'
        connection.send(str.encode(response))
        connection.close()
        return False

    for user in credentials:
        if name == str(user['user_name']) and bank_id == int(user['user_id']):
            response = 'Registration successful'
            connection.send(str.encode(response))
            registered = True
            return True
    
    if not registered:
        response = 'Registration error: incorrect credentials'
        connection.send(str.encode(response))
        connection.close()
        return False
    
    # SEND TRANSACTIONS TO BANK
    global transactions
    
    while True:
        for i in range(len(transactions)):
            connection.send(str.encode(transactions[i]))
            
def server():
    ServerSocketClient = socket.socket()
    ServerSocketBank = socket.socket()
    # declare host and port on which we need to communicate with clients
    ip = "127.0.0.1"
    port_client = 13370
    port_bank = 13371
    ThreadCountClient = ThreadCountBank = 0
    # if it binds successfully then it starts waiting for the client otherwise
    # it returns the error that occurred while establishing a connection
    try:
        ServerSocketClient.bind((ip, port_client))
        ServerSocketBank.bind((ip, port_bank))
    except socket.error as e:
        print(str(e))
    print('Waiting for a Connection..')

    # use a while loop to make it run Server endlessly until we manually stop the Server
    while True:
        ServerSocketClient.listen(1)
        ServerSocketBank.listen(2)
        if ServerSocketClient.accept():
            Client, address = ServerSocketClient.accept()
            print('Connected to client: ' + address[0] + ':' + str(address[1]))

            start_new_thread(threaded_client, (Client,))
            ThreadCountClient += 1
            print('Client Thread Number: ' + str(ThreadCountClient))
        
        if ServerSocketBank.accept():
            Bank, address = ServerSocketBank.accept()
            print('Connected to bank: ' + address[0] + ':' + str(address[1]))

            start_new_thread(threaded_bank, (Bank,))
            ThreadCountBank += 1
            print('Bank Thread Number: ' + str(ThreadCountBank))

    ServerSocket.close()
    
if __name__ == '__main__':
    server()
