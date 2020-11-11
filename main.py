# -*- coding: utf-8 -*-
import socket
import json


def server():
    host = socket.gethostname()
    ip = socket.gethostbyname(host)
    print(ip)
    port = 8080
    
    s = socket.socket()
    s.bind((ip, port))
    
    s.listen(1)
    
    while True:
        clientSocket, address = s.accept()
        print("Connection from ", str(address), " has been established! ")
        
        try:
            while True:
                data = clientSocket.recv(1024).decode('utf-8')
                if not data:
                    break
                print('from online user: ' + data)
                data = 'Hello World! Received data: ' + data
                clientSocket.send(data.encode('utf-8'))
        except socket.error as e:
            print("Exception caught for ", e.strerror)
        
        clientSocket.close()
        
def reading():
    my_config_file1 = open('data\config_1.json', 'r')
    my_config_file1 = my_config_file1.read()
    object1 = json.loads(my_config_file1)

    return object1

    
if __name__ == '__main__':
    obj1 = reading()
    ip = obj1['server']['ip']
    print('Retrieved IP address from JSON: ')
    print(ip)

    port = obj1['server']['port']
    print('Using port: ')
    print(port)

    print('-------------')
    server()
    

